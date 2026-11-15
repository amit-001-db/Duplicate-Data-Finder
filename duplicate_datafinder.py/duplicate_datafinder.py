import sys
import os

def find_duplicats(file_name: str = None, option: int= None, output_file: str= "unique.txt"):
    """
    Finds duplicate entries in a text file and writes unique entries to output_file.
    
    Parameters:
        file_name (str): Path to input file (defaults to user prompt or 'data.txt')
        option (int): 1 for Exact match, 2 for Ignore case and extra spaces
        output_file (str): Output file name for unique entries (default: 'unique.txt')
    """
    # ---------------------------------------------------------
    # 1. Obtain File Name
    # ---------------------------------------------------------
    if file_name is None:
        try:
            user_input = input("Enter file name: ").strip()
            file_name = user_input if user_input else "data.txt"
        except EOFError:
            file_name = "data.txt"

    # ---------------------------------------------------------
    # 2. Read entries with try-except (Requirement 2)
    # ---------------------------------------------------------
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            raw_lines = f.read().splitlines()
    except FileNotFoundError:
        print(f"File '{file_name}' not found. Please enter a valid file name.")
        return

    # Check for empty file (Test Case 3b)
    # If the file has no lines or consists solely of whitespace
    if len(raw_lines) == 0 or all(line.strip() == "" for line in raw_lines):
        print("File is empty. Nothing to check.")
        return

    # ---------------------------------------------------------
    # 3. Obtain Menu Option (Requirement 4)
    # ---------------------------------------------------------
    if option is None:
        print("\nMenu Options:")
        print("1. Exact match")
        print("2. Ignore case and extra spaces")
        try:
            choice = input("Enter choice (1/2): ").strip()
            if choice == "2":
                option = 2
            else:
                option = 1
        except EOFError:
            option = 1

     # ---------------------------------------------------------
    # 4. Prepare the list of entries based on chosen option
    # ---------------------------------------------------------
    entries = []
    if option == 2:
        # Option 2: Ignores case and extra spaces
        for line in raw_lines:
            # Strip leading/trailing spaces and collapse internal consecutive spaces
            cleaned = " ".join(line.split()).lower()
            if cleaned:
                entries.append(cleaned)
    else:
        # Option 1: Exact match
        for line in raw_lines:
            if line:
                entries.append(line)
    if not entries:
        print("File is empty. Nothing to check.")
        return

    # ---------------------------------------------------------
    # 5. Use a set to find unique entries & loop to count repeats
    #    (Requirement 3)
    # ---------------------------------------------------------
    # Use a set to find the unique entries
    unique_set = set(entries)
    # Preserve original order of first appearance
    unique_entries = []
    for item in entries:
        if item in unique_set and item not in unique_entries:
            unique_entries.append(item)
    # Use a loop to count how many times each entry repeats
    counts = {}
    for entry in unique_entries:
        count = 0
        for item in entries:
            if item == entry:
                count += 1
        counts[entry] = count

    # ---------------------------------------------------------
    # 6. Save unique entries to output file
    # ---------------------------------------------------------
    with open(output_file, "w", encoding="utf-8") as out:
        for item in unique_entries:
            out.write(f"{item}\n")

     # ---------------------------------------------------------
    # 7. Display Results (Requirement 5)
    # ---------------------------------------------------------
    total_items = len(entries)
    unique_items = len(unique_entries)
    # Line 1: Total items and Unique items
    print(f"Total items: {total_items} | Unique items: {unique_items}")
    # Identify duplicates (entries appearing > 1 time)
    duplicates = [(item, counts[item]) for item in unique_entries if counts[item] > 1]
    if duplicates:
        # Format: Duplicates: item (N times) | item2 (M times)
        dup_str = " | ".join(f"{item} ({cnt} times)" for item, cnt in duplicates)
        print(f"Duplicates: {dup_str}")
        print(f"Unique list saved to {output_file}")
    else:
        # Test Case 2 Output
        print("No duplicates found.")