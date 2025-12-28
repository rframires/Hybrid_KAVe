# main.py

import os
import sys
import time
import argparse
import traceback

# We'll import mlkg_assembler AFTER applying CLI flags to the environment
mlkg_mod = None

global count_xss
global count_sqli
statistics = []


def apply_env_flags_from_args(args):
    """Set environment flags so modules reading os.getenv at import time pick them up.

    Only sets variables explicitly provided (keeps existing env otherwise).
    """
    def set_flag(name: str, val):
        if val is not None:
            os.environ[name] = str(val)

    set_flag("MLKG_DEBUG", args.debug)
    set_flag("MLKG_GPT_ENABLED", args.gpt_enabled)
    set_flag("MLKG_GPT_ONLY", args.gpt_only)
    set_flag("MLKG_GPT_BATCH", args.gpt_batch)
    set_flag("MLKG_GPT_BATCH_SIZE", args.gpt_batch_size)
    set_flag("MLKG_GPT_INCLUDE_FILE", args.gpt_include_file)
    set_flag("MLKG_CSV_DEDUP", args.csv_dedup)


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Analyze PHP files or folders for XSS/SQLi")
    parser.add_argument("path", help="File or directory to analyze")
    # Back-compat: optional positional type as in previous versions
    parser.add_argument("type_pos", nargs="?", choices=["xss", "sqli", "all"], help=argparse.SUPPRESS)
    parser.add_argument("--type", choices=["xss", "sqli", "all"], default=None, help="Optional sink filter")

    # Optional flags (map to environment for downstream modules)
    parser.add_argument("--gpt-enabled", type=int, choices=[0, 1], default=None, help="Enable GPT advisor")
    parser.add_argument("--gpt-only", type=int, choices=[0, 1], default=None, help="Only count GPT findings")
    parser.add_argument("--gpt-batch", type=int, choices=[0, 1], default=None, help="Batch GPT items per file")
    parser.add_argument("--gpt-batch-size", type=int, default=None, help="Batch size for GPT items")
    parser.add_argument("--gpt-include-file", type=int, choices=[0, 1], default=None, help="Include full file in GPT prompts")
    parser.add_argument("--csv-dedup", type=int, choices=[0, 1], default=None, help="Deduplicate CSV across runs")
    parser.add_argument("--debug", type=int, choices=[0, 1], default=None, help="Enable debug logging")

    args = parser.parse_args(argv)
    # Resolve effective type: --type overrides positional if both provided
    args.effective_type = args.type if args.type is not None else args.type_pos
    return args


def main(path, type=False):

    start = time.perf_counter()

    # Import mlkg_assembler after env flags are set (in __main__)
    global mlkg_mod
    if mlkg_mod is None:
        import mlkg_assembler as _mlkg
        mlkg_mod = _mlkg

    # Checking if the path is a file or a directory
    if os.path.isfile(path):
        # If it's a file
        if path.endswith('.php'):
            # Process the single PHP file
            print(path)
            try:
                statistics.append(mlkg_mod.find_vuls(path[:-4], type))
            except Exception as e:
                print("Error processing file:", path)
                print(e)
                if os.getenv("MLKG_DEBUG", "0") == "1":
                    traceback.print_exc()
        else:
            print("The provided file is not a PHP file.")

    elif os.path.isdir(path):
        # If it's a directory
        # Recursively search for PHP files
        files = [os.path.join(root, filename)
                 for root, dirs, files in os.walk(path)
                 for filename in files
                 if filename.endswith('.php')]
        files.sort()

        for file in files:
            print(file)
            try:
                statistics.append(mlkg_mod.find_vuls(file[:-4], type))
            except Exception as e:
                print("Error processing file:", file)
                print(e)
                if os.getenv("MLKG_DEBUG", "0") == "1":
                    traceback.print_exc()
    else:
        print("The provided path does not exist.")

    load_vulstats()

    print("Total vulnerabilities found:\nXSS:", count_xss, "\nSQLi:", count_sqli)

    print_graphstats()

    end = time.perf_counter()
    elapsed = end - start
    print("\nElapsed time:", "{:.2f}".format(elapsed), "seconds")


def load_vulstats():
    try:
        global count_xss
        global count_sqli

        # Access counters from the imported module
        global mlkg_mod
        if mlkg_mod is None:
            import mlkg_assembler as _mlkg
            mlkg_mod = _mlkg
        count_xss = mlkg_mod.count_xss
        count_sqli = mlkg_mod.count_sqli

        # Return the loaded variables
        return count_xss, count_sqli
    except ImportError as e:
        print("Error loading MLKG variables:", e)
        return None, None
    
def print_graphstats():
    
    print("\nGraph stats:")
    print("N grafs:", sum([x[0] for x in statistics]))
    print("N functions:", sum([x[1] for x in statistics]))
    print("N variables:", sum([x[2] for x in statistics]))
    print("N nodes:", sum([x[3] for x in statistics]))
    print("N edges:", sum([x[4] for x in statistics]))

if __name__ == "__main__":
    # Parse CLI flags and apply environment before importing mlkg_assembler
    args = parse_args(sys.argv[1:])
    apply_env_flags_from_args(args)

    # Run
    main(args.path, args.effective_type)
 

#####Não me lembro o que faz este type

'''
Melhorar o CFG
Implementar os conectores
Tornar em objetos
'''