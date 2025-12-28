from openai import OpenAI
import os
import csv
import time

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_vulnerabilities(code_snippet, max_retries=3):
    """Analyze code with retry logic for transient failures"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a security expert. Consider if there is sanitization."},
                    {"role": "user", "content": f"Respond with only 'Safe' or 'Unsafe' based on whether this PHP code has XSS vulnerabilities:\n\n{code_snippet}"}
                ],
                temperature=0,
                max_tokens=10  # Keep max tokens low for short responses
            )
            
            # Directly return the content from the response
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # Exponential backoff: 2, 4, 6 seconds
                print(f"  [WARNING] API error (attempt {attempt + 1}/{max_retries}): {str(e)[:100]}")
                print(f"  [WAIT] Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise  # Re-raise on final attempt


def analyze_folder(folder_path, output_csv, vulnerability_type):
    print(f"\n{'='*60}")
    print(f"Starting analysis of: {folder_path}")
    print(f"Vulnerability type: {vulnerability_type}")
    print(f"Output file: {output_csv}")
    print(f"{'='*60}\n")
    
    # Open the CSV file in write mode
    with open(output_csv, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        # Write the header row
        writer.writerow(["Filename", "Result"])
        
        # Get list of files
        files = [f for f in os.listdir(folder_path) if f.endswith(".php")]
        total_files = len(files)
        print(f"Found {total_files} PHP files to analyze\n")
        
        # Loop through each file in the folder
        for idx, filename in enumerate(files, 1):
            file_path = os.path.join(folder_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as php_file:
                    php_code = php_file.read()
                    
                    # Analyze the file
                    result = analyze_vulnerabilities(php_code)
                    
                    # Print the result with progress
                    print(f"[{idx}/{total_files}] {filename}: {result}")
                    
                    # Write the result to the CSV file
                    writer.writerow([filename, result])
                    csv_file.flush()  # Ensure data is written immediately
                    
            except Exception as e:
                error_msg = f"ERROR - {str(e)}"
                print(f"[{idx}/{total_files}] {filename}: {error_msg}")
                writer.writerow([filename, error_msg])
                csv_file.flush()

    print(f"\n{'='*60}")
    print(f"[OK] Analysis complete: {folder_path}")
    print(f"[OK] Results saved to: {output_csv}")
    print(f"{'='*60}\n")


# TEST VERSION - Using Samples2 with only 10 files per folder
# Example usage for SQL Injection analysis
folder_path_sqli_unsafe = "../Samples2/SQLi_Unsafe/"
output_csv_sqli_unsafe = "../output/results_sqli_baseline_unsafe_test.csv"
analyze_folder(folder_path_sqli_unsafe, output_csv_sqli_unsafe, "SQLi")

folder_path_sqli_safe = "../Samples2/SQLi_Safe/"
output_csv_sqli_safe = "../output/results_sqli_baseline_safe_test.csv"
analyze_folder(folder_path_sqli_safe, output_csv_sqli_safe, "SQLi")

# Example usage for XSS analysis
folder_path_xss_unsafe = "../Samples2/XSS_Unsafe/"
output_csv_xss_unsafe = "../output/results_xss_baseline_unsafe_test.csv"
analyze_folder(folder_path_xss_unsafe, output_csv_xss_unsafe, "XSS")

folder_path_xss_safe = "../Samples2/XSS_Safe/"
output_csv_xss_safe = "../output/results_xss_baseline_safe_test.csv"
analyze_folder(folder_path_xss_safe, output_csv_xss_safe, "XSS")

# Final summary
print("\n" + "="*60)
print("  *** ALL ANALYSIS COMPLETE! ***")
print("="*60)
print("\nAll 4 folders have been analyzed:")
print(f"  [OK] {output_csv_sqli_unsafe}")
print(f"  [OK] {output_csv_sqli_safe}")
print(f"  [OK] {output_csv_xss_unsafe}")
print(f"  [OK] {output_csv_xss_safe}")
print("\nTest experiment completed successfully!")
print("="*60 + "\n")
