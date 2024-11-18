# VimWikiTodoer
Simple Python Script to manage vimwiki todos

# Vimwiki TODO Manager Setup Instructions

## Prerequisites

Before you begin, ensure you have the following:

1. **Python**: Make sure Python 3 is installed on your system. You can verify this by running:

    ```bash
    python --version
    ```

2. **Vimwiki**: Ensure that you have Vimwiki set up in your Vim configuration and your wiki directory is accessible.

3. **Required Libraries**: This program requires the `colorama` and `termcolor` libraries for colored output. You can install them using `pip`.

---

## Installation

Follow these steps to install and set up the program:

### 1. Clone the Repository (if applicable)

If this program is in a Git repository, clone it:

```bash
git clone https://github.com/yourusername/VimWikiTodoer.git
cd vimwiki-todo-manager
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage
### 1. Display all TODOs
To list all your TODOs from index.wiki and linked files:

```bash
python todo_manager.py --list
```
### 2. Toggle TODOs
To toggle (check off or uncheck) a specific TODO, use the --toggle argument with a comma-separated list of TODO numbers:
```bash
python todo_manager.py --toggle 1,3,5
```
### 3. Add a new TODO to a File
To add a new TODO to a file containing a specific substring in its name:

```bash
python todo_manager.py --add "file_substring:Your new task description"

```
For example, to add a TODO to a file with project in its name:
```bash
python todo_manager.py --add "project:Finish documentation"

```
### 4. Delete a Specific TODO
To delete a specific TODO, use the --delete argument with the TODO number:

```bash
python todo_manager.py --delete 3

```
### 5. Delete All Completed TODOs
```bash
python todo_manager.py --delete-completed
```