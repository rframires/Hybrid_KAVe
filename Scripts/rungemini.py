import os
import csv
from google import genai

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def analyze_vulnerabilities(code_snippet, vulnerability_type):
    if vulnerability_type == "SQLi":
        prompt = f"""
You are a Security Auditor specializing in web application vulnerabilities. Your task is to analyze PHP code for SQL Injection vulnerabilities.
- Check if user input is sanitized or validated before being used in database queries.
- Respond ONLY with 'Safe' if there are no vulnerabilities or 'Unsafe' if there are any vulnerabilities.

PHP Code:
{code_snippet}
"""
    elif vulnerability_type == "XSS":
        prompt = f"""
You are a Penetration Tester specializing in identifying Cross-Site Scripting (XSS) vulnerabilities. Your task is to analyze PHP code for XSS vulnerabilities.
- Check if user input is sanitized or escaped before being outputted to HTML.
- Respond ONLY with 'Safe' if there are no vulnerabilities or 'Unsafe' if there are any vulnerabilities.

PHP Code:
{code_snippet}
"""
    else:
        raise ValueError("Unsupported vulnerability type. Use 'SQLi' or 'XSS'.")

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    return response.text.strip()

def analyze_folder(folder_path, output_csv, vulnerability_type):
    with open(output_csv, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Filename", "Result"])

        for filename in os.listdir(folder_path):
            if filename.endswith(".php"):
                file_path = os.path.join(folder_path, filename)
                try:
                    with open(file_path, "r", encoding="utf-8") as php_file:
                        php_code = php_file.read()
                        result = analyze_vulnerabilities(php_code, vulnerability_type)
                        print(f"{filename}: {result}")
                        writer.writerow([filename, result])
                except Exception as e:
                    print(f"Error processing {filename}: {e}")

    print(f"Results saved to {output_csv}")
    
# Example usage for SQL Injection analysis
folder_path_sqli_safe = "../Samples/SQLi_Safe/"
output_csv_sqli_safe = "../output/results_sqli_safe_gemini.csv"
analyze_folder(folder_path_sqli_safe, output_csv_sqli_safe, "SQLi")

folder_path_sqli_unsafe = "../Samples/SQLi_Unsafe/"
output_csv_sqli_unsafe = "../output/results_sqli_unsafe_gemini.csv"
analyze_folder(folder_path_sqli_unsafe, output_csv_sqli_unsafe, "SQLi")

# Example usage for XSS analysis
folder_path_xss_safe = "../Samples/XSS_Safe/"
output_csv_xss_safe = "../output/results_xss_safe_gemini.csv"
analyze_folder(folder_path_xss_safe, output_csv_xss_safe, "XSS")

folder_path_xss_unsafe = "../Samples/XSS_Unsafe/"
output_csv_xss_unsafe = "../output/results_xss_unsafe_gemini.csv"
analyze_folder(folder_path_xss_unsafe, output_csv_xss_unsafe, "XSS")
