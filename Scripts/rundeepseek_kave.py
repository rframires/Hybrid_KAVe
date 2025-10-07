import subprocess
import os
import csv
from openai import OpenAI

client = OpenAI(api_key="add_api_key", base_url="https://api.deepseek.com")

# Function to run the external tool and get its output
def get_tool_output(file_path):
    try:
        # Run the external tool as a subprocess
        result = subprocess.run(
            ["python3", "KAVe3/main.py", file_path],  #Change path to KAVe main.py
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Return the tool's output or an error message if it fails
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error running tool: {result.stderr.strip()}"
    except Exception as e:
        return f"Exception occurred: {str(e)}"

# Function to analyze vulnerabilities with a combined approach
def analyze_vulnerabilities(code_snippet, vulnerability_type, tool_output):
    if vulnerability_type == "SQLi":
        prompt = f"""
You are a Security Auditor specializing in web application vulnerabilities. Your task is to analyze PHP code for SQL Injection vulnerabilities.
- Check if user input is sanitized or validated before being used in database queries.
- Use the following information from an external tool to guide your analysis:
{tool_output}
- Respond ONLY with 'Safe' if there are no vulnerabilities or 'Unsafe' if there are any vulnerabilities.

PHP Code:
{code_snippet}
"""
    elif vulnerability_type == "XSS":
        prompt = f"""
You are a Penetration Tester specializing in identifying Cross-Site Scripting (XSS) vulnerabilities. Your task is to analyze PHP code for XSS vulnerabilities.
- Check if user input is sanitized or escaped before being outputted to HTML.
- Use the following information from an external tool to guide your analysis:
{tool_output}
- Respond ONLY with 'Safe' if there are no vulnerabilities or 'Unsafe' if there are any vulnerabilities.

PHP Code:
{code_snippet}
"""
    else:
        raise ValueError("Unsupported vulnerability type. Use 'SQLi' or 'XSS'.")

    # Send the prompt to GPT
    response = client.chat.completions.create(
        model= "deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a security expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=10,  # Keep max tokens low for concise responses
        stream=False
    )

    # Return only the final result ('Safe' or 'Unsafe')
    return response.choices[0].message.content.strip()

# Function to analyze all files in a folder
def analyze_folder(folder_path, output_csv, vulnerability_type):
    with open(output_csv, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Filename", "Tool Output", "Result"])
        
        for filename in os.listdir(folder_path):
            if filename.endswith(".php"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r") as php_file:
                    php_code = php_file.read()
                    # Get external tool output for this file
                    tool_output = get_tool_output(file_path)
                    # Analyze the file
                    result = analyze_vulnerabilities(php_code, vulnerability_type, tool_output)
                    print(f"{filename}: {result}")
                    writer.writerow([filename, tool_output, result])
    
    print(f"Results saved to {output_csv}")

# Example usage for SQL Injection analysis
folder_path_sqli_safe = "Samples/SQLi_Safe/"
output_csv_sqli_safe = "results_sqli_safe_deepseek.csv"
analyze_folder(folder_path_sqli_safe, output_csv_sqli_safe, "SQLi")

folder_path_sqli_unsafe = "Samples/SQLi_Unsafe/"
output_csv_sqli_unsafe = "results_sqli_unsafe_deepseek.csv"
analyze_folder(folder_path_sqli_unsafe, output_csv_sqli_unsafe, "SQLi")

# Example usage for XSS analysis
folder_path_xss_safe = "Samples/XSS_Safe/"
output_csv_xss_safe = "results_xss_safe_deepseek.csv"
analyze_folder(folder_path_xss_safe, output_csv_xss_safe, "XSS")

folder_path_xss_unsafe = "Samples/XSS_Unsafe/"
output_csv_xss_unsafe = "results_xss_unsafe_deepseek.csv"
analyze_folder(folder_path_xss_unsafe, output_csv_xss_unsafe, "XSS")
