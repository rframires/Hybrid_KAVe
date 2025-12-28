import os
from typing import Optional, List, Dict

from agents import Agent

class GPTConclusionAgent(Agent):
    def __init__(self, agent_id: str, model: str = "gpt-4o"):
        super().__init__(agent_id)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        # Lazy import so the package is only required when GPT is enabled.
        from openai import OpenAI

        try:
            timeout_s = float(os.getenv("MLKG_GPT_TIMEOUT", "30"))
        except Exception:
            timeout_s = 30.0

        self.client = OpenAI(api_key=api_key, timeout=timeout_s)
        self.model = model
        self.temperature = 0.0
        # Conversation state per file
        self._file_messages: Optional[List[Dict[str, str]]] = None
        self._file_id: Optional[str] = None
        self._policy_text = self._build_policy()
        # Usage tracking and debug flag
        self._usage: Optional[Dict[str, int]] = None
        self._DEBUG_AI = os.getenv("MLKG_DEBUG", "0") == "1"
        # Control whether to include full PHP file in prompts
        self._INCLUDE_FILE = os.getenv("MLKG_GPT_INCLUDE_FILE", "1") == "1"

    def begin_file(self, file_id: str, php_code: str):
        """Start a per-file conversation; optionally include code once based on env flag."""
        code = php_code if len(php_code) < 4000 else php_code[:4000] + "\n...\n"
        self._file_id = file_id
        if self._INCLUDE_FILE:
            self._file_messages = [
                {"role": "system", "content": self._policy_text},
                {"role": "user", "content": f"FILE: {file_id}\nPHP_FILE (truncated to 4 000 chars):\n{code}"},
            ]
        else:
            self._file_messages = [
                {"role": "system", "content": self._policy_text},
                {"role": "user", "content": f"FILE: {file_id}\n(PHP file omitted per MLKG_GPT_INCLUDE_FILE=0)"},
            ]
        # init usage tracking
        self._usage = {"prompt": 0, "completion": 0, "total": 0, "calls": 0}
        if self._DEBUG_AI:
            try:
                if self._INCLUDE_FILE:
                    print(f"[DEBUG] GPT begin_file: {file_id}, code_chars={len(code)}")
                else:
                    print(f"[DEBUG] GPT begin_file: {file_id}, code_omitted=True")
            except Exception:
                pass

    def end_file(self):
        """Clear per-file conversation context and return usage summary."""
        usage = self._usage
        self._file_messages = None
        self._file_id = None
        self._usage = None
        return usage

    def analyse(self, entry, sink, path, php_code: Optional[str] = None, *,
                entry_line: Optional[int] = None,
                sink_line: Optional[int] = None,
                sanitization: Optional[str] = None,
                entry_snippet: Optional[str] = None,
                sink_snippet: Optional[str] = None) -> dict:
        if self._file_messages is not None:
            # Per-file chat: send only the question without resending code
            question = self._build_question(entry, sink, path,
                                            entry_line=entry_line,
                                            sink_line=sink_line,
                                            sanitization=sanitization,
                                            entry_snippet=entry_snippet,
                                            sink_snippet=sink_snippet)
            messages = list(self._file_messages) + [{"role": "user", "content": question}]
            rsp = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                messages=messages,
            )
        else:
            # Single-shot: include policy and code in one prompt
            prompt = self._build_prompt(entry, sink, path, php_code or "",
                                        entry_line=entry_line,
                                        sink_line=sink_line,
                                        sanitization=sanitization,
                                        entry_snippet=entry_snippet,
                                        sink_snippet=sink_snippet)
            rsp = self.client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                messages=[
                    {"role": "system", "content": self._policy_text},
                    {"role": "user", "content": prompt}
                ]
            )
        verdict = rsp.choices[0].message.content.strip()
        # Update usage if the API returned token info
        try:
            if hasattr(rsp, "usage") and rsp.usage is not None:
                u = rsp.usage
                pt = getattr(u, "prompt_tokens", 0) or 0
                ct = getattr(u, "completion_tokens", 0) or 0
                tt = getattr(u, "total_tokens", (pt or 0) + (ct or 0))
                if self._usage is None:
                    self._usage = {"prompt": 0, "completion": 0, "total": 0, "calls": 0}
                self._usage["prompt"] += int(pt)
                self._usage["completion"] += int(ct)
                self._usage["total"] += int(tt)
                self._usage["calls"] += 1
                if self._DEBUG_AI:
                    print(f"[DEBUG] GPT usage: prompt={pt}, completion={ct}, total={tt}")
        except Exception:
            pass
        return {"entry": entry, "sink": sink, "path": path, "verdict": verdict}

    def analyse_batch(self, items: list, path) -> list:
        """Analyse a list of entry→sink items in one request.

        Each item is a dict with keys: entry, sink, entry_line, sink_line, sanitization, entry_snippet, sink_snippet.
        Returns a list of dicts with the same order, each containing a 'verdict' field.
        """
        if not items:
            return []
        # Build a compact batch question
        header = (
            "You will be given multiple candidate data-flow pairs (entry→sink).\n"
            "For EACH item i, output exactly one line: i:[Vulnerable] or i:[Probably_safe] or i:[Needs_manual_review].\n"
            "No extra commentary before or after.\n"
        )
        parts = []
        for i, it in enumerate(items, start=1):
            entry = it.get("entry")
            sink = it.get("sink")
            entry_line = it.get("entry_line")
            sink_line = it.get("sink_line")
            sanit = it.get("sanitization") or "unknown"
            esnip = it.get("entry_snippet") or ""
            ssnip = it.get("sink_snippet") or ""
            parts.append(
                f"Item {i}:\n"
                f"ENTRY: {entry} (line {entry_line})\n"
                f"SINK: {sink} (line {sink_line})\n"
                f"SANITIZATION_DETECTED: {sanit}\n"
                f"ENTRY_SNIPPET:\n{esnip}\n\nSINK_SNIPPET:\n{ssnip}\n"
            )
        question = header + "\n".join(parts) + "\nRespond with one line per item as specified."

        if self._file_messages is not None:
            messages = list(self._file_messages) + [{"role": "user", "content": question}]
        else:
            # Single-shot with policy only; omit file unless env includes it
            messages = [
                {"role": "system", "content": self._policy_text},
                {"role": "user", "content": question},
            ]
        rsp = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages,
        )
        text = rsp.choices[0].message.content.strip()
        # Update usage
        try:
            if hasattr(rsp, "usage") and rsp.usage is not None:
                u = rsp.usage
                pt = getattr(u, "prompt_tokens", 0) or 0
                ct = getattr(u, "completion_tokens", 0) or 0
                tt = getattr(u, "total_tokens", (pt or 0) + (ct or 0))
                if self._usage is None:
                    self._usage = {"prompt": 0, "completion": 0, "total": 0, "calls": 0}
                self._usage["prompt"] += int(pt)
                self._usage["completion"] += int(ct)
                self._usage["total"] += int(tt)
                self._usage["calls"] += 1
                if self._DEBUG_AI:
                    print(f"[DEBUG] GPT usage (batch): prompt={pt}, completion={ct}, total={tt}")
        except Exception:
            pass

        # Parse lines like "1:[Vulnerable]"
        verdicts = [None] * len(items)
        try:
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                # support formats like "1: [Vulnerable]" or "1.[Vulnerable]"
                match = None
                import re as _re
                m = _re.match(r"^(\d+)\s*[:\.-]?\s*(\[[^\]]+\])", line)
                if m:
                    idx = int(m.group(1)) - 1
                    if 0 <= idx < len(items):
                        verdicts[idx] = m.group(2)
        except Exception:
            pass
        # Fallback: if parsing failed, mark as manual review
        for i, v in enumerate(verdicts):
            if not v:
                verdicts[i] = "[Needs_manual_review]"
        return [{"verdict": v} for v in verdicts]

    def _build_policy(self) -> str:
        return (
            "You are a senior application-security analyst.\n"
            "Decision policy:\n"
            "- Mark Vulnerable only if untrusted input can reach the sink without context-appropriate sanitization/validation and can change SQL/JS/HTML semantics.\n"
            "- Consider the specific context of use. Numeric-only inputs used in numeric SQL context (unquoted) after strict type casting or validation (e.g., (int), (float), intval, floatval, is_numeric, regex ^[0-9]+$) are Probably_safe for SQL injection.\n"
            "- Casting/validation is NOT sufficient if the value is concatenated inside quotes or later treated as a string in SQL.\n"
            "- Prepared statements/parameterization are safe. Addslashes alone is weak; prefer escaping suited to the API.\n"
            "- For XSS, only flag when untrusted data is rendered into HTML/JS without encoding; printing database results or numeric-only values typically does not enable script execution.\n"
            "- Avoid false positives: if the only user-controlled part is cast to a number and used unquoted in SQL, treat as Probably_safe unless other string concatenations enable injection.\n"
            "- If the code context is omitted or ambiguous, be conservative and prefer [Needs_manual_review] over [Vulnerable].\n"
            "Reply with one short sentence and end with exactly one of: [Vulnerable], [Probably_safe], [Needs_manual_review]."
        )

    def _build_prompt(self, entry, sink, path, php_code,
                       *, entry_line=None, sink_line=None,
                       sanitization=None, entry_snippet=None, sink_snippet=None) -> str:
        # keep the file reasonably small – trim after 4 000 chars
        code = php_code if len(php_code) < 4000 else php_code[:4000] + "\n...\n"

        entry_line_s = f"{entry_line}" if entry_line is not None else "unknown"
        sink_line_s = f"{sink_line}" if sink_line is not None else "unknown"
        sanit_s = sanitization or "unknown"
        esnip = entry_snippet or ""
        ssnip = sink_snippet or ""

        examples = (
            "Examples:\n"
            "1) $id = (int)$_GET['id']; $q = \"SELECT * FROM t WHERE id=$id\"; // Probably_safe (numeric, unquoted).\n"
            "2) $id = (int)$_GET['id']; $q = \"... WHERE id='$id'\"; // Vulnerable (inside quotes).\n"
            "3) echo $query; // Not XSS if $query contains only SQL with numbers; XSS only if untrusted HTML/JS is output.\n"
        )

        base = (
            examples + "\n" +
            f"ENTRY: {entry}  (line {entry_line_s})\n" +
            f"SINK:  {sink}   (line {sink_line_s})\n" +
            f"SANITIZATION_DETECTED: {sanit_s}\n" +
            f"PATH (top-down): {path}\n\n" +
            f"ENTRY_SNIPPET:\n{esnip}\n\n" +
            f"SINK_SNIPPET:\n{ssnip}\n\n"
        )
        if self._INCLUDE_FILE and code:
            base += "PHP_FILE (truncated to 4 000 chars):\n" + code + "\n\n"
        base += "Reply with one short sentence and end with exactly one of: [Vulnerable], [Probably_safe], [Needs_manual_review]."
        return base

    def _build_question(self, entry, sink, path,
                        *, entry_line=None, sink_line=None,
                        sanitization=None, entry_snippet=None, sink_snippet=None) -> str:
        entry_line_s = f"{entry_line}" if entry_line is not None else "unknown"
        sink_line_s = f"{sink_line}" if sink_line is not None else "unknown"
        sanit_s = sanitization or "unknown"
        esnip = entry_snippet or ""
        ssnip = sink_snippet or ""
        tail = "Reply with one short sentence and end with exactly one of: [Vulnerable], [Probably_safe], [Needs_manual_review]."
        if not self._INCLUDE_FILE:
            tail = (
                "Note: The full PHP file is omitted in this session. If uncertain due to missing context, prefer [Needs_manual_review] over [Vulnerable].\n"
                + tail
            )
        return (
            f"ENTRY: {entry}  (line {entry_line_s})\n"
            f"SINK:  {sink}   (line {sink_line_s})\n"
            f"SANITIZATION_DETECTED: {sanit_s}\n"
            f"PATH (top-down): {path}\n\n"
            f"ENTRY_SNIPPET:\n{esnip}\n\n"
            f"SINK_SNIPPET:\n{ssnip}\n\n"
            f"{tail}"
        )