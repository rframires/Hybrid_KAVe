from openai import OpenAI
import os
import csv

client = OpenAI() #Add API Key

def analyze_vulnerabilities(code_snippet):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a security expert. Consider if there is sanitization."},
            {"role": "user", "content": f"Analyze this PHP code for SQL Injection vulnerabilities. Check if user input is sanitized or escaped before being outputted. Respond only with 'Safe' if there are no vulnerabilities or 'Unsafe' if there are any vulnerabilities:\n\n{code_snippet}"}
        ],
        temperature=0,
        max_tokens=10  # Keep max tokens low for short responses
    )
    
    # Directly return the content from the response
    return response.choices[0].message.content.strip()


def analyze_folder(folder_path, output_csv):
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
                    result = analyze_vulnerabilities(php_code)
                    
                    # Print the result
                    print(f"{filename}: {result}")
                    
                    # Write the result to the CSV file
                    writer.writerow([filename, result])

    print(f"Results saved to {output_csv}")

# Example usage for SQL Injection analysis
folder_path_sqli_unsafe = "Samples/SQLi_Unsafe/"
output_csv_sqli_unsafe = "results_sqli_contextual_unsafe.csv"
analyze_folder(folder_path_sqli_unsafe, output_csv_sqli_unsafe, "SQLi")

folder_path_sqli_safe = "Samples/SQLi_Safe/"
output_csv_sqli_safe = "results_sqli_contextual_safe.csv"
analyze_folder(folder_path_sqli_safe, output_csv_sqli_safe, "SQLi")

# Example usage for XSS analysis
folder_path_xss_unsafe = "Samples/XSS_Unsafe/"
output_csv_xss_unsafe = "results_xss_contextual_unsafe.csv"
analyze_folder(folder_path_xss_unsafe, output_csv_xss_unsafe, "XSS")

folder_path_xss_safe = "Samples/XSS_Safe/"
output_csv_xss_safe = "results_xss_contextual_safe.csv"
analyze_folder(folder_path_xss_safe, output_csv_xss_safe, "XSS")
