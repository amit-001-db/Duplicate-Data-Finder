import os
import sys
from io import StringIO
from duplicate_datafinder import find_duplicats

def run_test(test_id, title, file_name, option, expected_in_output, output_file=None):
    print("=" * 65)
    print(f"[{test_id}] {title}")
    print(f"Input File: {file_name} | Option: {option}")
    print("-" * 65)
    
    # Capture standard output
    old_stdout = sys.stdout
    captured = StringIO()
    sys.stdout = captured
    
    try:
        if output_file:
            find_duplicats(file_name=file_name, option=option, output_file=output_file)
        else:
            find_duplicats(file_name=file_name, option=option)
    finally:
        sys.stdout = old_stdout
    
    output = captured.getvalue().strip()
    print("Actual Output:")
    print(output)
    
    # Verify expected strings
    all_passed = True
    for exp in expected_in_output:
        if exp not in output:
            all_passed = False
            print(f"FAILED: Expected '{exp}' not found in output.")
    
    if all_passed:
        print("\nResult: [PASS]")
    else:
        print("\nResult: [FAIL]")
    return all_passed

def main():
    print("\n" + "=" * 65)
    print("        DUPLICATE DATA FINDER - TEST CASE VERIFICATION        ")
    print("=" * 65)
    
    results = []
    
    # Test Case 1: Exact Match with Duplicates
    results.append(run_test(
        test_id="Test Case 1",
        title="Exact Match with Duplicates (Option 1)",
        file_name="test_cases/tc1_exact_duplicates.txt",
        option=1,
        expected_in_output=[
            "Total items: 6 | Unique items: 4",
            "Duplicates: Apple (2 times) | Banana (2 times)",
            "Unique list saved to unique.txt"
        ],
        output_file="unique.txt"
    ))
    
    # Test Case 2: No Duplicates
    results.append(run_test(
        test_id="Test Case 2",
        title="No Duplicates Found (Option 1)",
        file_name="test_cases/tc2_no_duplicates.txt",
        option=1,
        expected_in_output=[
            "Total items: 3 | Unique items: 3",
            "No duplicates found."
        ]
    ))
    
    # Test Case 3a: File Not Found Error Handling
    results.append(run_test(
        test_id="Test Case 3a",
        title="File Not Found Error Handling (Requirement 2)",
        file_name="test_cases/non_existent_file.txt",
        option=1,
        expected_in_output=[
            "File 'test_cases/non_existent_file.txt' not found. Please enter a valid file name."
        ]
    ))
    
    # Test Case 3b: Empty File Handling
    results.append(run_test(
        test_id="Test Case 3b",
        title="Empty File Handling",
        file_name="test_cases/tc3b_empty.txt",
        option=1,
        expected_in_output=[
            "File is empty. Nothing to check."
        ]
    ))
    
    # Test Case 4: Ignore Case and Extra Spaces
    results.append(run_test(
        test_id="Test Case 4",
        title="Ignore Case and Extra Spaces (Option 2)",
        file_name="test_cases/tc4_case_and_spaces.txt",
        option=2,
        expected_in_output=[
            "Total items: 4 | Unique items: 2",
            "Duplicates: data science (3 times)",
            "Unique list saved to unique.txt"
        ],
        output_file="unique.txt"
    ))
    
    print("\n" + "=" * 65)
    total = len(results)
    passed = sum(results)
    print(f"Summary: {passed}/{total} Test Cases Passed Successfully.")
    print("=" * 65 + "\n")
    
    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
