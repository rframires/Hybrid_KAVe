#!/usr/bin/env python3
"""
Interactive Experiment Runner for Hybrid KAVe
This script provides a menu-driven interface to run different experiments.
"""
import os
import sys
import subprocess
from datetime import datetime

# Get the base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, 'Scripts')
SAT_DIR = os.path.join(BASE_DIR, 'SAT')
SAMPLES_DIR = os.path.join(BASE_DIR, 'Samples')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')


def get_preferred_python_executable():
    """Return the Python executable to use for subprocesses.

    Prefer the workspace-local .venv interpreter when present so users don't need
    to activate a virtualenv manually. Fall back to the currently running interpreter.
    """
    if os.name == 'nt':
        candidate = os.path.join(BASE_DIR, '.venv', 'Scripts', 'python.exe')
    else:
        candidate = os.path.join(BASE_DIR, '.venv', 'bin', 'python')
    return candidate if os.path.exists(candidate) else sys.executable


PYTHON_EXE = get_preferred_python_executable()


def ensure_output_dir():
    """Ensure output directory exists."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)


def generate_output_filename(prefix, extension="txt"):
    """Generate a timestamped output filename."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(OUTPUT_DIR, f"{prefix}_{timestamp}.{extension}")


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def get_user_choice(options, prompt="Select an option: "):
    """
    Display options and get user's choice.
    
    Args:
        options: List of option strings
        prompt: Prompt message
    
    Returns:
        Selected option index (0-based)
    """
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")
    print(f"  0. Exit/Back")
    print()
    
    while True:
        try:
            choice = int(input(prompt))
            if 0 <= choice <= len(options):
                return choice
            else:
                print(f"Invalid choice. Please enter a number between 0 and {len(options)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_api_key(service_name):
    """
    Prompt user for API key.
    
    Args:
        service_name: Name of the service (e.g., 'OpenAI', 'Google Gemini', 'DeepSeek')
    
    Returns:
        API key string or None if skipped
    """
    print(f"\n{'='*60}")
    print(f"  API Key Required for {service_name}")
    print(f"{'='*60}")
    print("\nPlease enter your API key (or press Enter to skip):")
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("\nWarning: No API key provided. The script may fail if it requires authentication.")
        return None
    
    return api_key


def get_input_path():
    """
    Get input path from user with quick selection options (for snippets).
    
    Returns:
        Path string or None if cancelled
    """
    print("\nSelect input source:")
    
    quick_folders = [
        ("SQLi_Safe", os.path.join(SAMPLES_DIR, 'SQLi_Safe')),
        ("SQLi_Unsafe", os.path.join(SAMPLES_DIR, 'SQLi_Unsafe')),
        ("XSS_Safe", os.path.join(SAMPLES_DIR, 'XSS_Safe')),
        ("XSS_Unsafe", os.path.join(SAMPLES_DIR, 'XSS_Unsafe')),
        ("Enter custom path", None)
    ]
    
    options = [name for name, _ in quick_folders]
    choice = get_user_choice(options, "Select folder: ")
    
    if choice == 0:
        return None
    
    if choice == len(quick_folders):  # Custom path
        print("\nEnter the path to the folder or file to analyze:")
        input_path = input("Path: ").strip()
    else:
        input_path = quick_folders[choice - 1][1]
        print(f"\nSelected: {input_path}")
    
    if not input_path:
        print("No path provided.")
        return None
    
    # Check if path exists
    if not os.path.exists(input_path):
        print(f"\nError: Path does not exist: {input_path}")
        return None
    
    return input_path


def get_webapp_path():
    """
    Get web app path from user with quick selection options.
    
    Returns:
        Path string or None if cancelled
    """
    print("\nSelect web application to analyze:")
    
    webapp_dir = os.path.join(BASE_DIR, 'WebAppSample')
    
    # Find all folders and PHP files in WebAppSample
    webapp_items = []
    
    if os.path.exists(webapp_dir):
        # Get all subdirectories
        for item in os.listdir(webapp_dir):
            item_path = os.path.join(webapp_dir, item)
            if os.path.isdir(item_path):
                webapp_items.append((f"Folder: {item}", item_path))
        
        # Get all PHP files in subdirectories
        for root, dirs, files in os.walk(webapp_dir):
            for file in files:
                if file.endswith('.php'):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, webapp_dir)
                    webapp_items.append((f"File: {relative_path}", file_path))
    
    if not webapp_items:
        print(f"\nNo web applications found in {webapp_dir}")
        return None
    
    webapp_items.append(("Enter custom path", None))
    
    options = [name for name, _ in webapp_items]
    choice = get_user_choice(options, "Select web app: ")
    
    if choice == 0:
        return None
    
    if choice == len(webapp_items):  # Custom path
        print("\nEnter the path to the folder or file to analyze:")
        input_path = input("Path: ").strip()
    else:
        input_path = webapp_items[choice - 1][1]
        print(f"\nSelected: {input_path}")
    
    if not input_path:
        print("No path provided.")
        return None
    
    # Check if path exists
    if not os.path.exists(input_path):
        print(f"\nError: Path does not exist: {input_path}")
        return None
    
    return input_path


def run_snippet_script():
    """Run experiments on code snippets."""
    clear_screen()
    print_header("Run on Snippets - Select Script")
    
    # List all available scripts
    scripts = [
        "rundeepseek.py",
        "rundeepseek_kave.py",
        "rungemini.py",
        "rungemini_kave.py",
        "rungpt_baseline.py",
        "rungpt_chainofthought.py",
        "rungpt_combined.py",
        "rungpt_contextual.py",
        "rungpt_fewshot.py",
        "rungpt_kave.py",
        "rungpt_rolebased.py"
    ]
    
    choice = get_user_choice(scripts, "Select script to run: ")
    
    if choice == 0:
        return
    
    selected_script = scripts[choice - 1]
    script_path = os.path.join(SCRIPTS_DIR, selected_script)
    
    # Determine which API key is needed based on script name
    api_key = None
    env_vars = os.environ.copy()
    
    if 'gpt' in selected_script.lower():
        api_key = get_api_key('OpenAI GPT')
        if api_key:
            env_vars['OPENAI_API_KEY'] = api_key
    elif 'gemini' in selected_script.lower():
        api_key = get_api_key('Google Gemini')
        if api_key:
            env_vars['GOOGLE_API_KEY'] = api_key
            env_vars['GEMINI_API_KEY'] = api_key
    elif 'deepseek' in selected_script.lower():
        api_key = get_api_key('DeepSeek')
        if api_key:
            env_vars['DEEPSEEK_API_KEY'] = api_key
    
    # Ensure output directory exists
    ensure_output_dir()
    
    # Generate output filename
    script_name = selected_script.replace('.py', '')
    output_file = generate_output_filename(f"snippets_{script_name}")
    
    print(f"\nRunning {selected_script}...")
    print(f"Note: The script will analyze all samples in its predefined folders.")
    print(f"Output will be saved to: {output_file}")
    print("-" * 60)
    print()
    
    try:
        # Change to Scripts directory to run script (so relative paths work)
        original_dir = os.getcwd()
        os.chdir(SCRIPTS_DIR)
        
        # Open output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Experiment: {selected_script}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            f.flush()
            
            # Run with real-time output display and file writing
            process = subprocess.Popen(
                [PYTHON_EXE, selected_script],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                env=env_vars,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read and display output line by line
            for line in process.stdout:
                print(line, end='')
                f.write(line)
                f.flush()
            
            process.wait()
            
            if process.returncode != 0:
                error_msg = f"\n\nProcess exited with code {process.returncode}\n"
                print(error_msg)
                f.write(error_msg)
        
        # Return to original directory
        os.chdir(original_dir)
        
        print(f"\n\nResults saved to: {output_file}")
        print(f"\nNote: CSV result files have also been saved to the output/ directory.")
        
    except FileNotFoundError:
        print(f"\nScript not found: {script_path}")
        os.chdir(original_dir)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        os.chdir(original_dir)
    
    input("\nPress Enter to continue...")


def run_web_app_analysis():
    """Run experiments on web applications using SAT/main.py."""
    clear_screen()
    print_header("Run on Web Apps - KAVe Analysis")
    
    # Ask if they want GPT assistance or simple KAVe
    options = [
        "Simple KAVe (without GPT assistance)",
        "KAVe with GPT assistance"
    ]
    
    choice = get_user_choice(options, "Select analysis mode: ")
    
    if choice == 0:
        return
    
    use_gpt = (choice == 2)
    
    # Get API key if GPT assistance is selected
    api_key = None
    env_vars = os.environ.copy()
    
    if use_gpt:
        api_key = get_api_key('OpenAI GPT')
        if api_key:
            env_vars['OPENAI_API_KEY'] = api_key
    
    # Get web app path with quick selection
    web_app_path = get_webapp_path()
    
    if not web_app_path:
        input("\nPress Enter to continue...")
        return
    
    # Run main.py from SAT directory
    main_script = os.path.join(SAT_DIR, 'main.py')
    
    # Ensure output directory exists
    ensure_output_dir()
    
    # Generate output filename
    mode_suffix = "gpt" if use_gpt else "simple"
    output_file = generate_output_filename(f"webapp_kave_{mode_suffix}")
    
    print(f"\nRunning KAVe analysis on: {web_app_path}")
    print(f"Mode: {'With GPT assistance' if use_gpt else 'Simple KAVe'}")
    print(f"Output will be saved to: {output_file}")
    print("-" * 60)
    print()
    
    try:
        # Change to SAT directory to run main.py
        original_dir = os.getcwd()
        os.chdir(SAT_DIR)
        
        # Open output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Experiment: KAVe Web App Analysis\n")
            f.write(f"Mode: {'With GPT assistance' if use_gpt else 'Simple KAVe'}\n")
            f.write(f"Input Path: {web_app_path}\n")
            f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            f.flush()
            
            # Build command
            # SAT/main.py supports GPT via flags; positional args are reserved for sink type (xss/sqli/all).
            cmd = [PYTHON_EXE, 'main.py', web_app_path]
            if use_gpt:
                cmd.extend(['--gpt-enabled', '1'])
            
            # Run with real-time output display and file writing
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                env=env_vars,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read and display output line by line
            for line in process.stdout:
                print(line, end='')
                f.write(line)
                f.flush()
            
            process.wait()
            
            if process.returncode != 0:
                error_msg = f"\n\nProcess exited with code {process.returncode}\n"
                print(error_msg)
                f.write(error_msg)
        
        # Return to original directory
        os.chdir(original_dir)
        
        print(f"\n\nResults saved to: {output_file}")
        
    except subprocess.CalledProcessError as e:
        print(f"\nError running analysis: {e}")
        os.chdir(original_dir)
    except FileNotFoundError:
        print(f"\nMain script not found: {main_script}")
        os.chdir(original_dir)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        os.chdir(original_dir)
    
    input("\nPress Enter to continue...")


def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        clear_screen()
        print_header("Hybrid KAVe - Experiment Runner")
        
        options = [
            "Run on Snippets (select script from Scripts/)",
            "Run on Web Apps (using SAT/main.py)"
        ]
        
        choice = get_user_choice(options, "Select experiment type: ")
        
        if choice == 0:
            print("\nExiting...")
            sys.exit(0)
        elif choice == 1:
            run_snippet_script()
        elif choice == 2:
            run_web_app_analysis()


def main():
    """Main entry point."""
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)


if __name__ == "__main__":
    main()
