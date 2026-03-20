import argparse
import os
import sys
from core.scraper import fetch_test_cases
from core.judge import compile_cpp, run_test_case
from colorama import Fore, Style, init

# Initialize colorama for cross-platform terminal colors
init(autoreset=True)

def main():
    # 1. Set up the argument parser
    parser = argparse.ArgumentParser(description="CP Stress Tester & Scraper")
    parser.add_argument("url", help="The Codeforces problem URL")
    parser.add_argument("file", help="Path to your solution file (.cpp or .py)")
    
    args = parser.parse_args()
    url = args.url
    file_path = args.file

    # 2. Check if the solution file actually exists
    if not os.path.exists(file_path):
        print(Fore.RED + f"[!] Error: File '{file_path}' not found.")
        sys.exit(1)

    is_python = file_path.endswith('.py')
    is_cpp = file_path.endswith('.cpp')

    if not (is_python or is_cpp):
        print(Fore.RED + "[!] Error: Only .py and .cpp files are supported right now.")
        sys.exit(1)

    # 3. Compile if it's C++
    executable = file_path
    if is_cpp:
        executable = compile_cpp(file_path)
        if not executable:
            sys.exit(1) # Stop if compilation fails

    # 4. Scrape the test cases
    print(Fore.CYAN + "\n" + "="*40)
    print(Fore.CYAN + " SCRAPING TEST CASES")
    print(Fore.CYAN + "="*40)
    
    test_cases = fetch_test_cases(url)
    
    if not test_cases:
        print(Fore.RED + "[!] No test cases found or failed to fetch.")
        sys.exit(1)

    # 5. Run the tests
    print(Fore.CYAN + "\n" + "="*40)
    print(Fore.CYAN + " RUNNING TESTS")
    print(Fore.CYAN + "="*40)

    all_passed = True

    for i, case in enumerate(test_cases, 1):
        print(Style.BRIGHT + f"\n--- Test Case {i} ---")
        
        status_color, actual_output, time_taken = run_test_case(
            executable, case['input'], case['output'], is_python
        )

        print(f"Time: {time_taken:.3f}s")
        print(f"Status: {status_color}")
        
        # If it failed, print the diff so you can debug
        if "ACCEPTED" not in status_color:
            all_passed = False
            print("\nExpected:")
            print(case['output'])
            print("\nGot:")
            print(actual_output if actual_output else "[No Output]")

    # 6. Final Verdict
    print(Fore.CYAN + "\n" + "="*40)
    if all_passed:
        print(Fore.GREEN + Style.BRIGHT + "[*] ALL TEST CASES PASSED! Ready to submit! 🚀")
    else:
        print(Fore.RED + Style.BRIGHT + "[!] SOME TEST CASES FAILED. Check the logs above.")
    
    # 7. Cleanup the compiled binary (so your folder doesn't get cluttered)
    if is_cpp and os.path.exists(executable):
        os.remove(executable)
        print(Style.DIM + f"\n[*] Cleaned up compiled executable: {executable}")

if __name__ == "__main__":
    main()