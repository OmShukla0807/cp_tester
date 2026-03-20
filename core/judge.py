import subprocess
import time
import os
import sys
from colorama import Fore, Style, init

# Initialize colorama so colors work perfectly on Windows, Mac, and Linux
init(autoreset=True)

def compile_cpp(file_path):
    """Compiles a C++ file and returns the name of the executable."""
    print(f"[*] Compiling {file_path}...")
    
    # Decide the output executable name based on the operating system
    exe_name = "solution.exe" if os.name == 'nt' else "./solution.out"
    
    # Equivalent to typing: g++ -O2 file.cpp -o solution.exe
    compile_process = subprocess.run(
        ['g++', '-O2', file_path, '-o', exe_name.replace('./', '')], 
        capture_output=True, text=True
    )
    
    if compile_process.returncode != 0:
        print(Fore.RED + "[!] Compilation Error:\n" + compile_process.stderr)
        return None
        
    return exe_name

def run_test_case(executable, input_data, expected_output, is_python=False):
    """Feeds input to the executable, captures output, and verifies it."""
    # Set up the command depending on whether it's Python or C++
    command = [sys.executable, executable] if is_python else [executable]
    
    try:
        start_time = time.time()
        
        # Run the code, pass the input, and capture the output
        process = subprocess.run(
            command,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=3.0  # Force quit if it takes longer than 3 seconds (Infinite loop protection)
        )
        
        end_time = time.time()
        time_taken = end_time - start_time
        
        # Clean up whitespace/newlines to avoid silly mismatch errors
        actual_output = process.stdout.strip()
        expected_output = expected_output.strip()
        
        # Check for runtime errors (like segmentation faults or exceptions)
        if process.returncode != 0:
            return Fore.RED + "RUNTIME ERROR", process.stderr.strip(), time_taken
            
        # Check if the output matches the expected output
        if actual_output == expected_output:
            return Fore.GREEN + "ACCEPTED", actual_output, time_taken
        else:
            return Fore.RED + "WRONG ANSWER", actual_output, time_taken
            
    except subprocess.TimeoutExpired:
        return Fore.RED + "TIME LIMIT EXCEEDED", "", 3.0