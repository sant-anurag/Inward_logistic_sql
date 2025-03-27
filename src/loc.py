import os
import re

def count_lines_of_code(file_path):
    """Counts the executable code, comments, and total lines in a given Python file."""
    code_lines = 0
    comment_lines = 0
    total_lines = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped_line = line.strip()
            total_lines += 1
            if stripped_line.startswith("#") or stripped_line.startswith('"""') or stripped_line.startswith("'''"):
                comment_lines += 1
            elif stripped_line:  # Ignore empty lines
                code_lines += 1

    return code_lines, comment_lines, total_lines

# Set directory to the current directory
src_directory = "."

# Initialize totals
total_code = 0
total_comments = 0
total_loc = 0

# Store file-wise details
file_summary = []

print("File-wise Breakdown:")
print("-" * 50)

for root, _, files in os.walk(src_directory):
    for file in files:
        if file.endswith(".py"):  # Process only Python files
            file_path = os.path.join(root, file)
            code, comments, loc = count_lines_of_code(file_path)

            # Store for summary
            total_code += code
            total_comments += comments
            total_loc += loc

            # Print file-wise details
            print(f"{file_path}:")
            print(f"  Executable Code Lines: {code}")
            print(f"  Comment Lines: {comments}")
            print(f"  Total LOC: {loc}")
            print("-" * 50)

# Print overall summary
print("\nOverall Summary:")
print("=" * 50)
print(f"Total Executable Code Lines: {total_code}")
print(f"Total Comment Lines: {total_comments}")
print(f"Total LOC (Code + Comments): {total_loc}")
print("=" * 50)
