from openai import OpenAI
import os
import csv

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to analyze vulnerabilities with Chain-of-Thought reasoning
def analyze_vulnerabilities(code_snippet, vulnerability_type):
    # Define a Chain-of-Thought prompt for SQLi or XSS
    if vulnerability_type == "SQLi":
        prompt = f"""
Analyze this PHP code for SQL Injection vulnerabilities step by step:
1. Identify how user input is handled.
2. Determine if user input is sanitized or validated.
3. Check how user input is used in database queries.
4. Based on your analysis, respond with ONLY 'Safe' if there are no vulnerabilities or 'Unsafe' if there are any vulnerabilities.

PHP Code:
{code_snippet}
"""
    elif vulnerability_type == "XSS":
        prompt = f"""
Analyze this PHP code for Cross-Site Scripting (XSS) vulnerabilities step by step:
1. Identify where user input is accepted.
2. Determine if user input is sanitized or escaped before being outputted.
3. Check how user input is used in HTML output.
4. Based on your analysis, respond with ONLY 'Safe' if there are no vulnerabilities or 'Unsafe' if there are any vulnerabilities.

PHP Code:
{code_snippet}
"""
    else:
        raise ValueError("Unsupported vulnerability type. Use 'SQLi' or 'XSS'.")

    # Send the prompt to GPT
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a security expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0,
        max_tokens=10  # Allow more tokens for detailed reasoning
    )

    # Return only the final result ('Safe' or 'Unsafe')
    return response.choices[0].message.content.strip()

# Function to analyze all files in a folder
def analyze_folder(folder_path, output_csv, vulnerability_type):
    # Open the CSV file in write mode
    with open(output_csv, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row
        writer.writerow(["Filename", "Result"])

        # Loop through each file in the folder
        for filename in os.listdir(folder_path):
            # Process only .PHP files
            if filename.endswith(".php"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, "r") as php_file:
                    php_code = php_file.read()
                    # Analyze the file
                    result = analyze_vulnerabilities(php_code, vulnerability_type)
                    # Print and save the result
                    print(f"{filename}: {result}")
                    writer.writerow([filename, result])

    print(f"Results saved to {output_csv}")

# Example usage for SQL Injection analysis
folder_path_sqli_unsafe = "../Samples/SQLi_Unsafe/"
output_csv_sqli_unsafe = "../output/results_sqli_chain_unsafe.csv"
analyze_folder(folder_path_sqli_unsafe, output_csv_sqli_unsafe, "SQLi")

folder_path_sqli_safe = "../Samples/SQLi_Safe/"
output_csv_sqli_safe = "../output/results_sqli_chain_safe.csv"
analyze_folder(folder_path_sqli_safe, output_csv_sqli_safe, "SQLi")

# Example usage for XSS analysis
folder_path_xss_unsafe = "../Samples/XSS_Unsafe/"
output_csv_xss_unsafe = "../output/results_xss_chain_unsafe.csv"
analyze_folder(folder_path_xss_unsafe, output_csv_xss_unsafe, "XSS")

folder_path_xss_safe = "../Samples/XSS_Safe/"
output_csv_xss_safe = "../output/results_xss_chain_safe.csv"
analyze_folder(folder_path_xss_safe, output_csv_xss_safe, "XSS")
