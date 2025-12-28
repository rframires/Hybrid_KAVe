from openai import OpenAI
import os
import csv

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to analyze vulnerabilities with a combined approach
def analyze_vulnerabilities(code_snippet, vulnerability_type):
    # Define minimal examples and role-based prompts
    if vulnerability_type == "SQLi":
        examples = """
Here are examples of PHP code with and without SQL Injection vulnerabilities:
- Vulnerable: <?php $query = "SELECT * FROM users WHERE username = '" . $_POST['username'] . "'"; ?>
- Secure: <?php $stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?"); $stmt->execute([$_POST['username']]); ?>
"""
        prompt = f"""
You are a Security Auditor specializing in web application vulnerabilities. Your task is to analyze PHP code for SQL Injection vulnerabilities.
{examples}
Analyze this PHP code:
1. Check if user input is sanitized or validated before being used in database queries.
2. Respond ONLY with 'Safe' if there are no vulnerabilities or 'Unsafe' if there are any vulnerabilities.

PHP Code:
{code_snippet}
"""
    elif vulnerability_type == "XSS":
        examples = """
Here are examples of PHP code with and without Cross-Site Scripting (XSS) vulnerabilities:
- Vulnerable: <?php echo $_GET['name']; ?>
- Secure: <?php echo htmlspecialchars($_GET['name'], ENT_QUOTES, 'UTF-8'); ?>
"""
        prompt = f"""
You are a Penetration Tester specializing in identifying Cross-Site Scripting (XSS) vulnerabilities. Your task is to analyze PHP code for XSS vulnerabilities.
{examples}
Analyze this PHP code:
1. Check if user input is sanitized or escaped before being outputted to HTML.
2. Respond ONLY with 'Safe' if there are no vulnerabilities or 'Unsafe' if there are any vulnerabilities.

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
        max_tokens=10  # Keep max tokens low for concise responses
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
output_csv_sqli_unsafe = "../output/results_sqli_combined_unsafe.csv"
analyze_folder(folder_path_sqli_unsafe, output_csv_sqli_unsafe, "SQLi")

folder_path_sqli_safe = "../Samples/SQLi_Safe/"
output_csv_sqli_safe = "../output/results_sqli_combined_safe.csv"
analyze_folder(folder_path_sqli_safe, output_csv_sqli_safe, "SQLi")

# Example usage for XSS analysis
folder_path_xss_unsafe = "../Samples/XSS_Unsafe/"
output_csv_xss_unsafe = "../output/results_xss_combined_unsafe.csv"
analyze_folder(folder_path_xss_unsafe, output_csv_xss_unsafe, "XSS")

folder_path_xss_safe = "../Samples/XSS_Safe/"
output_csv_xss_safe = "../output/results_xss_combined_safe.csv"
analyze_folder(folder_path_xss_safe, output_csv_xss_safe, "XSS")
