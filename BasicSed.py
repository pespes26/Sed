import sys
import re

def sed_cases(commands, input_data, is_file=True):
    content = read_file(input_data) if is_file else input_data.splitlines(keepends=True)
    if content is None:
        return

    for command_text in commands:
        if command_text.startswith('s/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 4:
                original = parts[1]
                new = parts[2]
                content = sedSub(content, original, new)
            else:
                print("Invalid format for substitution. Expected format: s/original/new/")
                print_help()
                return
        elif command_text.startswith('d/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 3:
                word = parts[1]
                content = sedDelete(content, word)
            else:
                print("Invalid format for deletion. Expected format: d/word/")
                print_help()
                return
        elif command_text.startswith('a/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 4:
                pattern = parts[1]
                newtext = parts[2]
                content = sedAppend(content, pattern, newtext)
            else:
                print("Invalid format for appending. Expected format: a/pattern/newtext/")
                print_help()
                return
        elif command_text.startswith('i/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 4:
                pattern = parts[1]
                newtext = parts[2]
                content = sedInsert(content, pattern, newtext)
            else:
                print("Invalid format for inserting. Expected format: i/pattern/newtext/")
                print_help()
                return
        elif command_text == 'p':
            # Print the pattern space (file content)
            sedPrintPatternSpace(content)
        else:
            print("Invalid command.")
            print_help()
            return 1

    if is_file:
        write_file(input_data, content)
    else:
        return "".join(content)

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
        return content
    except FileNotFoundError:
        print(f"\nThe file '{file_path}' does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def write_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.writelines(content)
    except Exception as e:
        print(f"An error occurred: {e}")

def sedSub(content, original, new):
    # Replace the original string with the new string
    updated_content = [line.replace(original, new) for line in content]
    return updated_content

def sedDelete(content, word):
    # Delete lines containing the word
    updated_content = [line for line in content if word not in line]
    return updated_content

def sedAppend(content, pattern, newtext):
    # Append newtext after lines containing the pattern
    updated_content = []
    for line in content:
        updated_content.append(line)
        if pattern in line:
            updated_content.append(newtext + '\n')
    return updated_content

def sedInsert(content, pattern, newtext):
    # Insert newtext before lines containing the pattern
    updated_content = []
    for line in content:
        if pattern in line:
            updated_content.append(newtext + '\n')  # Insert new text
        updated_content.append(line)  # Append the original line
    return updated_content

def sedPrintPatternSpace(content):
    print("".join(content), end='')

def print_help():
    print("\nAvailable commands are:")
    print("'s': 'Substitute - Replace a pattern with a replacement. Expected format: 's/original/replacement/'")
    print("'a': 'Append - Append text after each line matched by a pattern. Expected format: 'a/pattern/newtext/'")
    print("'i': 'Insert - Insert text before each line matched by a pattern. Expected format: 'i/pattern/newtext/'")
    print("'d': 'Delete - Delete lines matching a pattern. Expected format: 'd/word/'")
    print("'p': 'Print - Print the entire pattern space (file content) to standard output. Expected format: 'p'")

def main():
    if len(sys.argv) < 4:
        print_help()
        return 1

    # Get the command-line arguments
    mode = sys.argv[1]
    command_text = sys.argv[2]
    input_data = sys.argv[3]
    
    # Split the commands by semicolons
    commands = command_text.split(';')
    
    if mode == '-f':
        # Process file input
        if read_file(input_data) is None:
            return 1
        sed_cases(commands, input_data, is_file=True)
    elif mode == '-s':
        # Process string input
        output = sed_cases(commands, input_data, is_file=False)
        if output:
            print(output)
    else:
        print("Invalid mode. Use '-f' for file mode or '-s' for string mode.")
        print_help()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
