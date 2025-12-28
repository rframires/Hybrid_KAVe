import pdg
import re
import networkx as nx
# Matplotlib is optional; only used for drawing when explicitly requested
try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None
from networkx.drawing import nx_agraph
import fcg
import agents
import os
import csv

kg = {}
functions = []
count_sqli = 0
count_xss = 0

# Flags controlled by environment variables
DEBUG_ASSEMBLER = os.getenv("MLKG_DEBUG", "0") == "1"
ENABLE_GPT_ONLY = os.getenv("MLKG_GPT_ONLY", "0") == "1"
# GPT is optional and disabled by default (requires network + OPENAI_API_KEY)
ENABLE_GPT = os.getenv("MLKG_GPT_ENABLED", "0") == "1"
GPT_BATCH = os.getenv("MLKG_GPT_BATCH", "0") == "1"
try:
    GPT_BATCH_SIZE = int(os.getenv("MLKG_GPT_BATCH_SIZE", "20"))
except Exception:
    GPT_BATCH_SIZE = 20

gpt_agent = None

def _ensure_gpt_agent():
    """Initialize GPT agent on-demand.

    Returns the agent instance or None if GPT is unavailable.
    """
    global gpt_agent, ENABLE_GPT
    if gpt_agent is not None:
        return gpt_agent
    if not ENABLE_GPT:
        return None
    try:
        from ai_agents import GPTConclusionAgent
        gpt_agent = GPTConclusionAgent("GPTConclusionAgent")
        return gpt_agent
    except Exception as _e:
        if DEBUG_ASSEMBLER:
            print("[DEBUG] GPT init failed, disabling GPT:", _e)
        ENABLE_GPT = False
        gpt_agent = None
        return None

def removeComments(file_path, return_mapping=False):
    with open(file_path, 'r', encoding='utf8', errors='ignore') as file:
        original_lines = file.readlines()

    processed_lines = []
    line_mapping = []
    in_block = False

    for idx, raw in enumerate(original_lines, start=1):
        line = raw.rstrip('\n')
        cur = line

        # Handle ongoing block comment
        if in_block:
            end_pos = cur.find('*/')
            if end_pos != -1:
                cur = cur[end_pos+2:]
                in_block = False
            else:
                # whole line is within a block comment
                continue

        # Remove all inline block comment segments; if it starts a block without end, mark and truncate
        while True:
            start_pos = cur.find('/*')
            if start_pos == -1:
                break
            end_pos = cur.find('*/', start_pos+2)
            if end_pos != -1:
                cur = cur[:start_pos] + cur[end_pos+2:]
            else:
                cur = cur[:start_pos]
                in_block = True
                break

        # Remove single-line comments (// ...)
        slash_pos = cur.find('//')
        if slash_pos != -1:
            cur = cur[:slash_pos]

        stripped = cur.strip()
        if stripped:
            processed_lines.append(stripped)
            line_mapping.append(idx)

    if return_mapping:
        # Return original file as list without trailing newlines for snippet indexing
        return processed_lines, line_mapping, [ln.rstrip('\n') for ln in original_lines]
    return processed_lines

def remove_html_comments(lines):
    in_comment = False
    cleaned_lines = []

    for line in lines:
        if '<!--' in line:
            in_comment = True
            continue
        elif '-->' in line:
            in_comment = False
            continue
        
        if not in_comment:
            cleaned_lines.append(line)

    return cleaned_lines

# Remove // … and /* … */ but keep every line-break / indent
def get_code_without_comments(file_path: str) -> str:
    with open(file_path, "r", encoding="utf8", errors="ignore") as fh:
        code = fh.read()

    # multi-line + single-line comments
    pattern = r"//.*?$|/\*.*?\*/"
    return re.sub(pattern, "", code, flags=re.MULTILINE | re.DOTALL)


def is_sanitized(node):
    """Safely determine if a node (entry/sink or nested) indicates sanitization.

    Accepts tuples/lists like (label, var, line, meta), plain strings, or nested structures.
    Never raises on unexpected shapes.
    """
    try:
        # tuple/list: (label, var, line, meta)
        if isinstance(node, (list, tuple)):
            label = node[0] if len(node) > 0 else None
            if isinstance(label, str) and "sanitization" in label:
                return True
            # Recurse into meta if present
            if len(node) > 3 and node[3]:
                return is_sanitized(node[3])
            return False

        # dict: check explicit key or any nested values
        if isinstance(node, dict):
            if node.get("sanitization"):
                return True
            for v in node.values():
                if is_sanitized(v):
                    return True
            return False

        # str: direct containment check
        if isinstance(node, str):
            return "sanitization" in node

        # Fallback for other types
        return False
    except Exception:
        return False

def find_vuls(path, type = False):

    global kg
    global functions
    global count_sqli
    global count_xss

    # Preserve display file path before local variables may shadow 'path'
    file_path_display = f"{path}.php"

    # Get processed lines with mapping to original line numbers
    processed_lines, processed_to_original_map, original_lines = removeComments(path + ".php", return_mapping=True)
    file = remove_html_comments(processed_lines)

    # Update mapping after HTML comment removal
    final_mapping = []
    html_in = False
    for i, line in enumerate(processed_lines):
        if '<!--' in line:
            html_in = True
            continue
        if '-->' in line:
            html_in = False
            continue
        if not html_in:
            final_mapping.append(processed_to_original_map[i])

    processed_to_original_map = final_mapping

    # Prepare string versions of code
    code = "\n".join(file)                 # processed, comment-stripped
    original_code_str = "\n".join(original_lines)  # original file content with original line order

    # Build function call graph once and reuse
    g = fcg.to_fcg(path + ".php", False)
    kg = {}
    functions = {}
    # Track processed->original line mappings per function name
    function_line_mappings = {}
    main = []

    nodes = [x[0] for x in list(g.nodes.data())]

    pilha = -1
    rem = False
    main_indices = []
    for i, l in enumerate(file):
        x = re.search("^function", l)
        if x:
            if l.count("{") == 0:
                rem = True
            pilha = 1
        elif pilha > 0:
            if rem:
                rem = False
                pilha -= 1
            pilha += l.count("{")
            pilha -= l.count("}")
        if pilha == 0:
            pilha = -1
        elif pilha == -1:
            main.append(l)
            main_indices.append(i)

    functions["_main"] = main
    # Build line mapping for main function using recorded indices
    main_line_mapping = [processed_to_original_map[idx] if idx < len(processed_to_original_map) else 0 for idx in main_indices]
    function_line_mappings["_main"] = main_line_mapping
    kg["_main"] = pdg.to_pdg(main, False, main_line_mapping)

    if DEBUG_ASSEMBLER:
        print("[DEBUG] Processed lines:", processed_lines)
        print("[DEBUG] Processed to original map:", processed_to_original_map)
        print("[DEBUG] Original lines:", original_lines)
        print("[DEBUG] main_indices:", main_indices)
        print("[DEBUG] main_line_mapping:", main_line_mapping)
        print("[DEBUG] function_line_mappings:", function_line_mappings)

    for n in nodes[1:]:

        pilha = -1
        function = []
        func_line_indices = []  # track which processed line each function line corresponds to
        for idx, l in enumerate(file):
            x = re.search("^function.*"+ n, l)
            if x:
                pilha = 1
                function.append(l)
                func_line_indices.append(idx)
            elif pilha > 0:
                pilha += l.count("{")
                pilha -= l.count("}")
                function.append(l)
                func_line_indices.append(idx)
            if pilha == 0:
                functions[n] = function
                # Build line mapping for this function
                func_line_mapping = [processed_to_original_map[i] if i < len(processed_to_original_map) else 0 
                                     for i in func_line_indices]
                function_line_mappings[n] = func_line_mapping
                p = pdg.to_pdg(function, False, func_line_mapping)
                kg[n] = p
                if len(p[1]) == 0 and not p[2]:
                    g.remove_node(n)
                #elif len(p[1]) == 0:
                #    kg[n] = p + "connector"
                else:
                    kg[n] = p
                break

    grafos = sum([x[3] + 2 for x in kg.values()]) + 1
    funcoes = len(functions)
    variaveis = sum([x[3] for x in kg.values()])
    nos = sum([len(x[0].nodes()) for x in kg.values()]) + len(g.nodes())
    edges = sum([len(x[0].edges()) for x in kg.values()]) + len(g.edges())

    possible_vulnerabilities = []
    vulnerabilities = []
    csv_rows = []
    # Per-file summary flags
    local_xss_found = False
    local_sqli_found = False

    agents.load_mlkg()

    # If GPT is enabled, run the GPT advisor.
    # (Previously it only ran in debug or "GPT-only" mode, which made the UI's "GPT assistance" option appear inactive.)
    run_gpt = ENABLE_GPT
    if run_gpt:
        agent = _ensure_gpt_agent()
        if agent is None:
            # Be explicit so users know GPT was not used.
            print("[WARN] GPT assistance was enabled but could not be initialized (check OPENAI_API_KEY and that the 'openai' package is installed).")
            run_gpt = False
        else:
            try:
                agent.begin_file(file_path_display, original_code_str)
            except Exception:
                # If begin_file fails, proceed without GPT.
                run_gpt = False

    for func in kg:
        if plt is not None:
            colors = nx.get_edge_attributes(kg[func][0],'color').values()
            nx.draw(kg[func][0], with_labels = True, edge_color=colors)
        if len(kg[func][1]) > 0:
            for y in [z for z in kg[func][1] if z[0] == "entry_point"]:
                    if not is_sanitized(y):
                        # Map original source line to PDG index within function for traversal
                        try:
                            orig_line = y[2] if len(y) > 2 and isinstance(y[2], int) else None
                            mapping = function_line_mappings.get(func, [])
                            pdg_index = mapping.index(orig_line) if (orig_line is not None and orig_line in mapping) else 0
                        except Exception:
                            pdg_index = 0

                        entry_for_travel = (y[0], y[1], pdg_index)
                        travel_agent = agents.TravelAgent("Travel Agent", g, kg, entry_for_travel)
                        possible_vulnerabilities += travel_agent.start_traversal([func])
                        if y[3] and "sink" in y[3][0] and (not type or y[3] and type in y[3][0]):
                            vulnerabilities.append((True, y, y, func))
                            if "xss" in y[3][0]:
                                count_xss+=1
                            if "sqli" in y[3][0]:
                                count_sqli+=1

    # Prepare collection for optional GPT batch
    gpt_items = []
    gpt_items_keys = set()
    # run_gpt already computed above

    for trial in possible_vulnerabilities:
        for sink in trial[1]:
            if not type or type in sink[0]:
                if not is_sanitized(sink):
                    verification_agent = agents.VerificationAgent(0, trial[0], sink, trial[2])
                    vres = verification_agent.start_verification(trial[2], trial[0][1])
                    if isinstance(vres, list):
                        if DEBUG_ASSEMBLER:
                            for _vr in vres:
                                try:
                                    ok = bool(_vr[0])
                                    e = _vr[1] if len(_vr) > 1 else None
                                    s = _vr[2] if len(_vr) > 2 else None
                                    print(f"[DEBUG] verify: {ok} entry={e} sink={s}")
                                except Exception:
                                    pass
                        vulnerabilities.extend(vres)
                    else:
                        if DEBUG_ASSEMBLER:
                            try:
                                ok = bool(vres[0]) if isinstance(vres, (list, tuple)) and vres else False
                                e = vres[1] if len(vres) > 1 else None
                                s = vres[2] if len(vres) > 2 else None
                                print(f"[DEBUG] verify: {ok} entry={e} sink={s}")
                            except Exception:
                                pass
                        vulnerabilities.append(vres)

                # ---------------- GPT-4o verdict ---------------- #
                # compute original entry line (trial[0][2] is PDG index within func)
                try:
                    func_ctx = trial[2][0] if trial[2] else "_main"
                except Exception:
                    func_ctx = "_main"
                mapping = function_line_mappings.get(func_ctx, [])
                entry_idx = trial[0][2] if len(trial[0]) > 2 else None
                entry_orig_line = mapping[entry_idx] if (isinstance(entry_idx, int) and 0 <= entry_idx < len(mapping)) else None
                sink_orig_line = sink[2] if len(sink) > 2 and isinstance(sink[2], int) else None

                # build small context snippets (±6 lines) from original file
                # Larger window helps include nearby casts/validations (e.g., (int)/(float))
                def snippet_at(line_no, window=6):
                    if not isinstance(line_no, int):
                        return ""
                    start = max(1, line_no - window)
                    end = min(len(original_lines), line_no + window)
                    lines = [f"{i:>4}: {original_lines[i-1]}" for i in range(start, end + 1)]
                    return "\n".join(lines)

                entry_snip = snippet_at(entry_orig_line)
                sink_snip = snippet_at(sink_orig_line)

                sanit_flag = "on entry" if is_sanitized(trial[0]) else ("on sink" if is_sanitized(sink) else "none")

                if run_gpt:
                    # Skip obvious constant-only XSS sinks to save tokens
                    sink_code_line = (original_lines[sink_orig_line-1] if isinstance(sink_orig_line, int) and 1 <= sink_orig_line <= len(original_lines) else "")
                    if isinstance(sink[0], str) and "xss" in sink[0]:
                        if '$' not in sink_code_line:
                            # no dynamic variable in echo/print line
                            continue
                    # Deduplicate GPT items by (entry_line, sink_line, sink_type)
                    key = (entry_orig_line, sink_orig_line, sink[0] if len(sink)>0 else None)
                    if key in gpt_items_keys:
                        continue
                    gpt_items_keys.add(key)
                    gpt_items.append({
                        "entry": (trial[0][0], trial[0][1], entry_orig_line),
                        "sink": (sink[0], sink[1] if len(sink)>1 else None, sink_orig_line),
                        "path": trial[2],
                        "entry_line": entry_orig_line,
                        "sink_line": sink_orig_line,
                        "sanitization": sanit_flag,
                        "entry_snippet": entry_snip,
                        "sink_snippet": sink_snip,
                        "_trial": trial,
                        "_sink": sink,
                    })

    # If batching is enabled, send all GPT items in one or more batches
    if run_gpt and GPT_BATCH and gpt_items:
        batches = [gpt_items[i:i+GPT_BATCH_SIZE] for i in range(0, len(gpt_items), GPT_BATCH_SIZE)]
        for batch in batches:
            try:
                results = _ensure_gpt_agent().analyse_batch(batch, path=None)
            except Exception as e:
                if DEBUG_ASSEMBLER:
                    print("[DEBUG] GPT analyse_batch() failed:", str(e))
                results = [{"verdict": "[Needs_manual_review]"} for _ in batch]
            for it, res in zip(batch, results):
                verdict = (res or {}).get("verdict", "")
                if DEBUG_ASSEMBLER:
                    print("GPT-4o verdict (batch):", verdict)
                if ENABLE_GPT_ONLY and "[Vulnerable]" in verdict:
                    vulnerabilities.append((
                        True,
                        it.get("entry"),           # correct entry tuple
                        it.get("_sink"),           # sink tuple from traversal
                        it.get("path"),            # path context
                        it.get("path"),            # pathprint reuse
                        "GPT detected",
                        verdict
                    ))
        # Clear items after batching
        gpt_items = []

    # If batching is disabled but GPT is requested, fall back to per-pair calls
    if run_gpt and not GPT_BATCH and gpt_items:
        for it in gpt_items:
            try:
                gpt_summary = _ensure_gpt_agent().analyse(
                    it["entry"], it["sink"], it["path"], php_code=None,
                    entry_line=it["entry_line"], sink_line=it["sink_line"],
                    sanitization=it["sanitization"],
                    entry_snippet=it["entry_snippet"], sink_snippet=it["sink_snippet"]
                )
            except Exception as e:
                if DEBUG_ASSEMBLER:
                    print("[DEBUG] GPT analyse() failed:", str(e))
                gpt_summary = {"verdict": "[Needs_manual_review]"}
            if DEBUG_ASSEMBLER:
                print("GPT-4o verdict:", gpt_summary.get("verdict", ""))
            if ENABLE_GPT_ONLY and "[Vulnerable]" in gpt_summary.get("verdict", ""):
                vulnerabilities.append((
                    True,
                    it.get("entry"),
                    it.get("_sink"),
                    it.get("path"),
                    it.get("path"),
                    "GPT detected",
                    gpt_summary.get("verdict", "")
                ))

    vuls = len([x for x in vulnerabilities if x[0]])

    # Prepare code lines for context/snippets
    # code_lines refers to original file lines so snippets can show original source
    code_lines = original_lines

    # Build a mask of comment-only lines in the original file to filter out spurious entries
    def build_comment_mask(lines):
        mask = set()
        in_block = False
        for i, raw in enumerate(lines, start=1):
            line = raw
            cur = line
            # detect single-line // comments
            stripped = cur.lstrip()
            if not in_block and stripped.startswith('//'):
                mask.add(i)
                continue
            # handle block comments /* ... */
            if in_block:
                mask.add(i)
                if '*/' in cur:
                    in_block = False
                continue
            if '/*' in cur:
                mask.add(i)
                if '*/' not in cur:
                    in_block = True
                else:
                    # same-line open/close still considered comment
                    pass
                continue
            # non-comment code line -> do nothing
        return mask

    comment_line_mask = build_comment_mask(code_lines)

    def get_snippet(line_no):
        try:
            if not line_no:
                return ""
            return code_lines[line_no - 1].strip()
        except Exception:
            return ""

    def extract_entry(entry):
        # entry expected like ('entry_point', '$var', line, meta)
        if not entry:
            return (None, None, None)
        var = entry[1] if len(entry) > 1 else None
        line = entry[2] if len(entry) > 2 and isinstance(entry[2], int) else None
        
        # Try to extract actual source from metadata (e.g., $_GET, $_POST)
        actual_source = None
        if len(entry) > 3 and entry[3]:
            meta = entry[3]
            if isinstance(meta, str):
                actual_source = meta
            elif isinstance(meta, (list, tuple)) and meta:
                actual_source = str(meta[0]) if meta[0] else None
        
        return (var, line, actual_source)

    def extract_sink(sink):
        # sink expected like ('sqli_sink', ('$query',), line, maybe_meta)
        if not sink:
            return (None, None, None)
        
        # Try to get function name from metadata or code
        func_name = None
        var_name = None
        sink_type = sink[0] if len(sink) > 0 else None
        
        # First try: get variable name from position 1
        if len(sink) > 1 and isinstance(sink[1], (list, tuple)) and sink[1]:
            var_name = sink[1][0]
        
        # Try to extract function name from metadata
        if len(sink) > 3 and sink[3]:
            meta = sink[3]
            if isinstance(meta, (list, tuple)) and meta:
                func_name = meta[0] if meta[0] else None
            elif isinstance(meta, str):
                func_name = meta
        
        line = sink[2] if len(sink) > 2 and isinstance(sink[2], int) else None
        
        # No code parsing: use detector-provided metadata or sink type
        if not func_name:
            if sink_type:
                func_name = sink_type
            elif var_name:
                func_name = var_name
        
        return (func_name, line, var_name)

    def sanitized_display(node):
        try:
            return is_sanitized(node)
        except Exception:
            return False

    # Pretty-print vulnerabilities
    printed = 0
    seen_keys = set()
    for vul in vulnerabilities:
        if not vul or not vul[0]:
            continue

        entry = vul[1] if len(vul) > 1 else None
        sink = vul[2] if len(vul) > 2 else None
        ctx_path = vul[3] if len(vul) > 3 else []

        entry_var, entry_idx, entry_source = extract_entry(entry)
        sink_name, sink_idx, sink_var = extract_sink(sink)

        # Determine function context
        func_ctx = None
        if isinstance(ctx_path, list) and ctx_path:
            func_ctx = ctx_path[0]
        elif isinstance(ctx_path, str) and ctx_path:
            func_ctx = ctx_path
        else:
            func_ctx = "_main"

        # Map PDG-local index back to original line if needed
        def to_original_line(func_name, idx_value, fallback=None):
            if idx_value is None:
                return fallback
            mapping = function_line_mappings.get(func_name, [])
            if 0 <= idx_value < len(mapping):
                return mapping[idx_value]
            return idx_value  # already original or out of range; display as-is

        entry_line = to_original_line(func_ctx, entry_idx, entry_idx)
        sink_line = sink_idx  # sink lines are original from DVG

        # Skip spurious findings where entry or sink lines resolve into comment-only lines
        if isinstance(entry_line, int) and entry_line in comment_line_mask:
            continue
        if isinstance(sink_line, int) and sink_line in comment_line_mask:
            continue

        # Deduplicate by (entry_line, sink_line, sink_name)
        dedupe_key = (entry_line, sink_line, sink_name)
        if dedupe_key in seen_keys:
            continue
        seen_keys.add(dedupe_key)

        # Line numbers now come directly from dvg/pdg with original file line numbers
        # No need to remap here anymore

        if sanitized_display(entry):
            sanit_detected = "Detected (on entry)"
        elif sanitized_display(sink):
            sanit_detected = "Detected (on sink)"
        else:
            sanit_detected = "None detected"

        printed += 1
        print(f"Vulnerability #{printed}")
        
        # Prefer showing the superglobal source (e.g., $_GET) from the original source line
        entry_display = None
        snippet_e = get_snippet(entry_line) if entry_line else ""
        if snippet_e:
            for ep in agents.entry_points:
                if ep in snippet_e:
                    entry_display = ep
                    break
        # If not found in snippet, use provided entry_source unless it's a function name like _main
        if not entry_display:
            if isinstance(entry_source, str) and not entry_source.startswith("_"):
                entry_display = entry_source
            else:
                entry_display = entry_var
        print(f"Entry point: {entry_display} (line {entry_line})")
        if snippet_e:
            print(f"  -> Source code: {snippet_e}")

        # Show function name for sink (extracted from code if possible)
        print(f"Sensitive sink: {sink_name} (line {sink_line})")
        snippet_s = get_snippet(sink_line) if sink_line else ""
        if snippet_s:
            print(f"  -> Sink code: {snippet_s}")

        print(f"Sanitization function: {sanit_detected}")

        if entry_line and sink_line:
            print(f"Data flow pairs: <line {entry_line}, line {sink_line}>")

        if len(vul) > 5 and vul[5] == "GPT detected":
            print("Detection note: flagged by GPT analysis")

        try:
            if sink and isinstance(sink[0], str):
                if "xss" in sink[0]:
                    count_xss += 1
                if "sqli" in sink[0]:
                    count_sqli += 1
        except Exception:
            pass

        print("")  # blank line between reports

        # Collect CSV row for this vulnerability
        try:
            csv_rows.append({
                "file": file_path_display,
                "entry": entry_display if entry_display else (entry_var or ""),
                "entry_line": entry_line if entry_line is not None else "",
                "sink": sink_name or "",
                "sink_line": sink_line if sink_line is not None else "",
                "sanitized": "Yes" if ("Detected" in sanit_detected) else "No",
                "detection_note": (vul[5] if len(vul) > 5 else ""),
                "gpt_verdict": (vul[6] if len(vul) > 6 else ""),
            })
        except Exception:
            pass

    print(f"Vulnerabilities detected: {printed}")
    print("\n")

    # Write CSV if any rows were collected
    try:
        if csv_rows:
            out_dir = os.path.join(os.getcwd(), "AI_results")
            os.makedirs(out_dir, exist_ok=True)
            out_csv = os.path.join(out_dir, "vulnerabilities.csv")
            write_header = not os.path.exists(out_csv)
            dedup_enabled = os.getenv("MLKG_CSV_DEDUP", "0") == "1"

            # Migrate header to include new columns if needed
            desired_fields = [
                "file", "entry", "entry_line", "sink", "sink_line", "sanitized", "detection_note", "gpt_verdict"
            ]
            if os.path.exists(out_csv):
                try:
                    with open(out_csv, mode="r", encoding="utf-8", newline="") as rf:
                        reader = csv.reader(rf)
                        existing_rows = list(reader)
                    if existing_rows:
                        existing_header = existing_rows[0]
                        if set(desired_fields) - set(existing_header):
                            with open(out_csv, mode="w", encoding="utf-8", newline="") as wf:
                                w = csv.writer(wf)
                                w.writerow(desired_fields)
                                for r in existing_rows[1:]:
                                    if len(r) < len(desired_fields):
                                        r = r + [""] * (len(desired_fields) - len(r))
                                    elif len(r) > len(desired_fields):
                                        r = r[:len(desired_fields)]
                                    w.writerow(r)
                            write_header = False
                except Exception:
                    # If migration fails, proceed; file will have mixed headers
                    pass
            if dedup_enabled:
                # Load existing rows and deduplicate across runs using a stable key
                existing: list[dict] = []
                try:
                    if os.path.exists(out_csv):
                        with open(out_csv, mode="r", newline="", encoding="utf-8") as rf:
                            reader = csv.DictReader(rf)
                            for r in reader:
                                existing.append({k: r.get(k, "") for k in desired_fields})
                except Exception as e:
                    if DEBUG_ASSEMBLER:
                        print("[DEBUG] Failed to read existing vulnerabilities.csv for dedup:", e)
                def key_of(d):
                    return (
                        str(d.get("file", "")),
                        str(d.get("entry_line", "")),
                        str(d.get("sink_line", "")),
                        str(d.get("sink", "")),
                    )
                seen = {key_of(r) for r in existing}
                appended = 0
                for row in csv_rows:
                    k = key_of(row)
                    if k not in seen:
                        existing.append(row)
                        seen.add(k)
                        appended += 1
                try:
                    with open(out_csv, mode="w", newline="", encoding="utf-8") as wf:
                        writer = csv.DictWriter(wf, fieldnames=desired_fields)
                        writer.writeheader()
                        for r in existing:
                            writer.writerow(r)
                    if DEBUG_ASSEMBLER:
                        print(f"[DEBUG] vulnerabilities.csv dedup applied, appended {appended} new unique rows")
                except Exception as e:
                    if DEBUG_ASSEMBLER:
                        print("[DEBUG] Failed to write deduped vulnerabilities.csv:", e)
            else:
                with open(out_csv, mode="a", newline="", encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=[
                        "file", "entry", "entry_line", "sink", "sink_line", "sanitized", "detection_note", "gpt_verdict"
                    ])
                    if write_header:
                        writer.writeheader()
                    for row in csv_rows:
                        writer.writerow(row)
    except Exception as csv_exc:
        if DEBUG_ASSEMBLER:
            print("[DEBUG] Failed to write CSV:", csv_exc)

    # Derive per-file flags from printed findings as a fallback
    try:
        if not local_xss_found:
            local_xss_found = any('xss' in str(row.get('sink', '')) for row in csv_rows)
        if not local_sqli_found:
            local_sqli_found = any('sqli' in str(row.get('sink', '')) for row in csv_rows)
    except Exception:
        pass

    # Write per-file summary CSV: file,xss,sqli where values are 0 (safe) or 1 (vulnerable)
    try:
        out_dir = os.path.join(os.getcwd(), "AI_results")
        os.makedirs(out_dir, exist_ok=True)
        summary_csv = os.path.join(out_dir, "file_summary.csv")
        write_header = not os.path.exists(summary_csv)
        dedup_enabled = os.getenv("MLKG_CSV_DEDUP", "0") == "1"
        row_obj = {
            "file": file_path_display,
            "xss": 1 if local_xss_found else 0,
            "sqli": 1 if local_sqli_found else 0,
        }
        if dedup_enabled and os.path.exists(summary_csv):
            # Replace existing row for this file
            existing_rows = []
            try:
                with open(summary_csv, mode="r", newline="", encoding="utf-8") as rf:
                    reader = csv.DictReader(rf)
                    for r in reader:
                        if r.get("file") != file_path_display:
                            existing_rows.append({"file": r.get("file", ""),
                                                  "xss": int(r.get("xss", 0) or 0),
                                                  "sqli": int(r.get("sqli", 0) or 0)})
            except Exception as e:
                if DEBUG_ASSEMBLER:
                    print("[DEBUG] Failed to read file_summary.csv for dedup:", e)
            existing_rows.append(row_obj)
            try:
                with open(summary_csv, mode="w", newline="", encoding="utf-8") as wf:
                    writer = csv.DictWriter(wf, fieldnames=["file", "xss", "sqli"])
                    writer.writeheader()
                    for r in existing_rows:
                        writer.writerow(r)
                if DEBUG_ASSEMBLER:
                    print("[DEBUG] file_summary.csv dedup applied (replaced existing row for file)")
            except Exception as e:
                if DEBUG_ASSEMBLER:
                    print("[DEBUG] Failed to write deduped file_summary.csv:", e)
        else:
            with open(summary_csv, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["file", "xss", "sqli"])
                if write_header:
                    writer.writeheader()
                writer.writerow(row_obj)
    except Exception as csv2_exc:
        # Robust fallback: ensure directory exists and retry; if still failing, rebuild from vulnerabilities
        try:
            if DEBUG_ASSEMBLER:
                print("[DEBUG] Failed to write file summary CSV:", csv2_exc)
                print("[DEBUG] Retrying after ensuring directory exists...")
            out_dir = os.path.join(os.getcwd(), "AI_results")
            os.makedirs(out_dir, exist_ok=True)
            summary_csv = os.path.join(out_dir, "file_summary.csv")
            # Try a minimal append write
            with open(summary_csv, mode="a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["file", "xss", "sqli"])
                if os.stat(summary_csv).st_size == 0:
                    writer.writeheader()
                writer.writerow({
                    "file": file_path_display,
                    "xss": 1 if local_xss_found else 0,
                    "sqli": 1 if local_sqli_found else 0,
                })
        except Exception as csv2_retry_exc:
            if DEBUG_ASSEMBLER:
                print("[DEBUG] Retry failed for file summary CSV:", csv2_retry_exc)
                print("[DEBUG] Attempting rebuild from vulnerabilities.csv as fallback...")
            # Final fallback: rebuild summary from vulnerabilities.csv so the file exists
            try:
                from parse_output import rebuild_summary_from_vulnerabilities_csv
                rebuild_summary_from_vulnerabilities_csv()
            except Exception as rebuild_exc:
                if DEBUG_ASSEMBLER:
                    print("[DEBUG] Fallback rebuild failed:", rebuild_exc)

    # End GPT per-file session
    if ENABLE_GPT:
        try:
            usage = gpt_agent.end_file()
            if DEBUG_ASSEMBLER and usage:
                print(f"[DEBUG] GPT per-file usage for {file_path_display}: calls={usage.get('calls')}, prompt_tokens={usage.get('prompt')}, completion_tokens={usage.get('completion')}, total_tokens={usage.get('total')}")
        except Exception:
            pass

    return (grafos, funcoes, variaveis, nos, edges, vuls > 0)
