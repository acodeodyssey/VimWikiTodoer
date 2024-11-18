import re
import os
import argparse
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

# Define Gruvbox colors in RGB
COLORS = {
    'bg': (60, 56, 54),     # Background (Dark Gray)
    'fg': (235, 219, 178),  # Foreground (Light Gray)
    'yellow': (215, 153, 33),
    'green': (184, 187, 38),
    'red': (251, 73, 52),
    'blue': (131, 165, 152),
    'purple': (211, 134, 155),
    'aqua': (142, 192, 124),
}
# Path to your Vimwiki file
VIMWIKI_DIR = os.path.expanduser("YOUR_PATH_HERE/vimwiki")
INDEX_FILE = os.path.join(VIMWIKI_DIR, "index.wiki")

def rgb_to_ansi(color):
    """Convert RGB to ANSI escape sequence for colorama"""
    return f'\033[38;2;{color[0]};{color[1]};{color[2]}m'

def find_linked_files():
    """Parse index.wiki for linked files and return their paths."""
    linked_files = []
    link_pattern = r"\[\[([^\]]+)\]\]"  # Matches Vimwiki links: [[filename]]
    with open(INDEX_FILE, "r") as file:
        for line in file:
            match = re.findall(link_pattern, line)
            if match:
                for link in match:
                    # Convert link to file path
                    if not link.endswith(".wiki"):
                        link += ".wiki"
                    linked_files.append(os.path.join(VIMWIKI_DIR, link))
    return linked_files

def load_todos_from_file(file_path):
    """Load TODOs from a single Vimwiki file."""
    todos = []
    with open(file_path, "r") as file:
        lines = file.readlines()
        for idx, line in enumerate(lines):
            match = re.match(r"^\s*-\s\[( |x)\]\s(.+)", line)
            if match:
                todos.append((file_path, idx, match.group(1), match.group(2)))  # (file, line number, status, text)
    return todos, lines

def load_all_todos():
    """Load TODOs from index.wiki and all linked files."""
    todos = []
    all_lines = {}
    files_to_check = [INDEX_FILE] + find_linked_files()

    for file_path in files_to_check:
        file_todos, lines = load_todos_from_file(file_path)
        todos.extend(file_todos)
        all_lines[file_path] = lines

    return todos, all_lines

def toggle_todo_in_file(file_path, line_idx, lines):
    """Toggle a TODO item in a specific file."""
    line = lines[line_idx]
    if "[ ]" in line:
        lines[line_idx] = line.replace("[ ]", "[x]")
    elif "[x]" in line:
        lines[line_idx] = line.replace("[x]", "[ ]")

    # Write changes back to the file
    with open(file_path, "w") as file:
        file.writelines(lines)

def delete_todo_in_file(file_path, line_idx, lines):
    """Delete a TODO item from a specific file."""
    del lines[line_idx]

    # Write changes back to the file
    with open(file_path, "w") as file:
        file.writelines(lines)

def display_todos(todos):
    """Display all TODOs in a numbered list with Gruvbox theme colors."""
    print(f"{rgb_to_ansi(COLORS['yellow'])}{Style.BRIGHT}Your TODOs:{Style.RESET_ALL}")
    for i, (file, line_idx, status, text) in enumerate(todos, start=1):
        checkbox = "[ ]" if status == " " else "[x]"
        checkbox_colored = rgb_to_ansi(COLORS['green']) + checkbox if status == 'x' else rgb_to_ansi(COLORS['red']) + checkbox
        relative_file = os.path.relpath(file, VIMWIKI_DIR)
        print(f"{rgb_to_ansi(COLORS['blue'])}{i}. {checkbox_colored} {text} ({rgb_to_ansi(COLORS['aqua'])}{relative_file}:{line_idx + 1})")

def toggle_multiple_todos(todo_numbers, todos, all_lines):
    """Toggle multiple TODOs based on their numbers."""
    for num in todo_numbers:
        if 1 <= num <= len(todos):
            file_path, line_idx, _, _ = todos[num - 1]
            toggle_todo_in_file(file_path, line_idx, all_lines[file_path])
            print(f"{rgb_to_ansi(COLORS['green'])}TODO #{num} updated!{Style.RESET_ALL}")
        else:
            print(f"{rgb_to_ansi(COLORS['red'])}Invalid TODO number: {num}{Style.RESET_ALL}")

def delete_todo_by_number(todo_number, todos, all_lines):
    """Delete a specific TODO based on its number."""
    if 1 <= todo_number <= len(todos):
        file_path, line_idx, _, _ = todos[todo_number - 1]
        delete_todo_in_file(file_path, line_idx, all_lines[file_path])
        print(f"{rgb_to_ansi(COLORS['red'])}TODO #{todo_number} deleted!{Style.RESET_ALL}")
    else:
        print(f"{rgb_to_ansi(COLORS['red'])}Invalid TODO number: {todo_number}{Style.RESET_ALL}")

def delete_all_completed_todos(todos, all_lines):
    """Delete all completed TODOs."""
    completed_todos = [todo for todo in todos if todo[2] == "x"]  # Filter for completed TODOs
    for file_path, line_idx, _, _ in completed_todos:
        delete_todo_in_file(file_path, line_idx, all_lines[file_path])
    print(f"{rgb_to_ansi(COLORS['red'])}{len(completed_todos)} completed TODO(s) deleted!{Style.RESET_ALL}")

def find_file_by_substring(substring):
    """Find a file in the Vimwiki directory based on a substring in the filename."""
    matching_files = []
    for root, dirs, files in os.walk(VIMWIKI_DIR):
        for file in files:
            if file.endswith(".wiki") and substring in file:
                matching_files.append(os.path.join(root, file))
    return matching_files

def add_todo_to_file(substring, todo_text):
    """Find a file by a substring and add a new TODO item to it."""
    matching_files = find_file_by_substring(substring)

    if not matching_files:
        print(f"{rgb_to_ansi(COLORS['red'])}No files found matching substring: {substring}{Style.RESET_ALL}")
        return

    # If multiple files are found, let the user choose one
    if len(matching_files) > 1:
        print(f"{rgb_to_ansi(COLORS['yellow'])}Multiple files found:{Style.RESET_ALL}")
        for idx, file in enumerate(matching_files, start=1):
            print(f"{rgb_to_ansi(COLORS['blue'])}{idx}. {file}")
        choice = input("Enter the number of the file you want to add the TODO to: ")
        try:
            chosen_file = matching_files[int(choice) - 1]
        except (ValueError, IndexError):
            print(f"{rgb_to_ansi(COLORS['red'])}Invalid choice.{Style.RESET_ALL}")
            return
    else:
        chosen_file = matching_files[0]

    with open(chosen_file, "a") as file:
        file.write(f"\n- [ ] {todo_text}\n")
    print(f"{rgb_to_ansi(COLORS['green'])}New TODO added to {chosen_file}: {todo_text}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description="Manage Vimwiki TODOs")
    parser.add_argument("--list", action="store_true", help="Display all TODOs")
    parser.add_argument("--toggle", type=str, help="Comma-separated TODO numbers to toggle")
    parser.add_argument("--add", type=str, help="Add a new TODO to a file matching substring (substring:todo_text)")
    parser.add_argument("--delete", type=int, help="Delete a specific TODO by number")
    parser.add_argument("--delete-completed", action="store_true", help="Delete all completed TODOs")

    args = parser.parse_args()


    args = parser.parse_args()
    todos, all_lines = load_all_todos()

    if not todos:
        print("No TODOs found!")
        return

    if args.list:
        display_todos(todos)

    if args.toggle:
        try:
            todo_numbers = [int(n) for n in args.toggle.split(",")]
            toggle_multiple_todos(todo_numbers, todos, all_lines)
        except ValueError:
            print("Invalid input! Please provide TODO numbers as a comma-separated list.")
    if args.add:
        try:
            substring, todo_text = args.add.split(":", 1)
            add_todo_to_file(substring, todo_text)
        except ValueError:
            print("Invalid format for --add. Use: --add substring:todo_text")
    if args.delete is not None:
        delete_todo_by_number(args.delete, todos, all_lines)

    if args.delete_completed:
        delete_all_completed_todos(todos, all_lines)

if __name__ == "__main__":
    main()