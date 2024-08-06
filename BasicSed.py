import sys
import re

# Global hold space
hold_space = ""

def sed_cases(commands, input_data, is_file=True):
    """
    Process a series of sed-like commands on given input data.

    Args:
        commands (list): A list of commands to execute.
        input_data (str): The path to the file or the input string to process.
        is_file (bool): Flag indicating whether input_data is a file path or a direct string.

    Returns:
        None if is_file is True.
        str if is_file is False, representing the processed string.
    """
    if is_file:
        content = read_file(input_data)
    else:
        content = input_data.splitlines(keepends=True)

    if content is None:
        return 1

    if not content:
        print("\nInput content is empty.")
        return 1

    for command_text in commands:
        if command_text.startswith('s/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 4:
                original = parts[1]
                new = parts[2]
                changed_lines = [line for line in content if re.search(re.escape(original), line)]
                if not changed_lines:
                    print(f"\nThe word '{original}' not found in the content.")
                    continue
                print(f"\nSubstituting '{original}' with '{new}'. Changed lines:")
                for line in changed_lines:
                    print(line, end='')
                content = sedSub(content, original, new)
            else:
                print("\nInvalid format for substitution. Expected format: s/original/new/")
                print_help()
                return
        elif command_text.startswith('d/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 3:
                pattern = parts[1]
                deleted_lines = [line for line in content if re.search(re.escape(pattern), line)]
                if not deleted_lines:
                    print(f"\nNo lines containing the pattern '{pattern}' found in the content.")
                    continue
                print(f"\nDeleting lines containing the pattern '{pattern}':")
                for line in deleted_lines:
                    print(line, end='')
                content = sedDelete(content, pattern)
            else:
                print("\nInvalid format for deletion. Expected format: d/pattern/")
                print_help()
                return
        elif command_text.startswith('a/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 4:
                pattern = parts[1]
                newtext = parts[2]
                if not any(re.search(re.escape(pattern), line) for line in content):
                    print(f"\nNo lines containing the pattern '{pattern}' found in the content.")
                    continue
                print(f"\nAppending '{newtext}' after lines containing pattern '{pattern}':")
                content = sedAppend(content, pattern, newtext)
                for line in content:
                    if re.search(re.escape(pattern), line):
                        print(line, end='')
            else:
                print("\nInvalid format for appending. Expected format: a/pattern/newtext/")
                print_help()
                return
        elif command_text.startswith('i/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 4:
                pattern = parts[1]
                newtext = parts[2]
                if not any(re.search(re.escape(pattern), line) for line in content):
                    print(f"\nNo lines containing the pattern '{pattern}' found in the content.")
                    continue
                print(f"\nInserting '{newtext}' before lines containing pattern '{pattern}':")
                content = sedInsert(content, pattern, newtext)
                for line in content:
                    if re.search(re.escape(pattern), line):
                        print(line, end='')
            else:
                print("\nInvalid format for inserting. Expected format: i/pattern/newtext/")
                print_help()
                return
        elif command_text == 'g':
            content = sedReplacePatternSpace(content)
        elif command_text == 'G':
            content = sedAppendHoldSpace(content)
        elif command_text == 'h':
            sedReplaceHoldSpace(content)
        elif command_text == 'H':
            sedAppendPatternToHoldSpace(content)
        elif command_text == 'l':
            sedWritePatternSpace(content)
        elif command_text.startswith('p/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 3:
                pattern = parts[1]
                matched_lines = [line for line in content if re.search(re.escape(pattern), line)]
                if not matched_lines:
                    print(f"\nPattern '{pattern}' not found in the content.")
                else:
                    print(f"\nPrinting lines matching pattern '{pattern}':")
                    for line in matched_lines:
                        print(line, end='')
            else:
                print("Invalid format for print matching lines. Expected format: p/pattern/")
                print_help()
                return
        elif command_text == 'P':
            sedPrintPatternSpaceUpToNewline(content)
        elif command_text == "q":
            print("Quitting the script")
            sys.exit(0)
        elif command_text.startswith(':'):
            continue
        elif command_text == 'L':
            print_help()
        else:
            print("Invalid command.")
            print_help()
            return 1

    if is_file and input_data:
        write_file(input_data, content)
    else:
        return "".join(content)

    # Final print of the entire content after all commands are executed
    print("\nContent:")
    sedPrintPatternSpace(content)

def read_file(file_path):
    """
    Read the content of a file.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        list: A list of lines read from the file.
    """
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
    """
    Write content to a file.

    Args:
        file_path (str): The path to the file to write.
        content (list): A list of lines to write to the file.
    """
    try:
        with open(file_path, 'w') as file:
            file.writelines(content)
    except Exception as e:
        print(f"An error occurred: {e}")

def sedSub(content, original, new):
    """
    Substitute occurrences of the original pattern with the new pattern.

    Args:
        content (list): The content to process.
        original (str): The pattern to replace.
        new (str): The replacement pattern.

    Returns:
        list: The updated content with substitutions.
    """
    original_escaped = re.escape(original)
    updated_content = [re.sub(original_escaped, new, line) for line in content]
    return updated_content

def sedDelete(content, pattern):
    """
    Delete lines containing the given pattern.

    Args:
        content (list): The content to process.
        pattern (str): The pattern to search for.

    Returns:
        list: The updated content with lines containing the pattern deleted.
    """
    pattern_escaped = re.escape(pattern)
    updated_content = [line for line in content if not re.search(pattern_escaped, line)]
    return updated_content

def sedAppend(content, pattern, newtext):
    """
    Append newtext after lines containing the given pattern.

    Args:
        content (list): The content to process.
        pattern (str): The pattern to search for.
        newtext (str): The text to append after matching lines.

    Returns:
        list: The updated content with newtext appended after matching lines.
    """
    pattern_escaped = re.escape(pattern)
    updated_content = []
    for line in content:
        updated_content.append(line)
        if re.search(pattern_escaped, line):
            updated_content.append(newtext + '\n')
    return updated_content

def sedInsert(content, pattern, newtext):
    """
    Insert newtext before lines containing the given pattern.

    Args:
        content (list): The content to process.
        pattern (str): The pattern to search for.
        newtext (str): The text to insert before matching lines.

    Returns:
        list: The updated content with newtext inserted before matching lines.
    """
    pattern_escaped = re.escape(pattern)
    updated_content = []
    for line in content:
        if re.search(pattern_escaped, line):
            updated_content.append(newtext + '\n')
        updated_content.append(line)
    return updated_content

def sedAppendHoldSpace(content):
    """
    Append the hold space contents to each line in the pattern space.

    Args:
        content (list): The content to process.

    Returns:
        list: The updated content with hold space contents appended to each line.
    """
    global hold_space
    hold_space_content = ''.join(hold_space) if isinstance(hold_space, list) else hold_space
    updated_content = []
    for line in content:
        updated_content.append(line.rstrip() + '\n' + hold_space_content)
    return updated_content

def sedReplaceHoldSpace(content):
    """
    Replace the hold space with the pattern space contents.

    Args:
        content (list): The content to process.
    """
    global hold_space
    hold_space = ''.join(content)
    print("\nHold space updated.")

def sedReplacePatternSpace(content):
    """
    Replace the pattern space with the hold space contents.

    Args:
        content (list): The content to process.

    Returns:
        list: The updated content with hold space contents replacing the pattern space.
    """
    global hold_space
    hold_space_content = ''.join(hold_space) if isinstance(hold_space, list) else hold_space
    updated_content = hold_space_content.splitlines(keepends=True)
    return updated_content if updated_content else [""]

def sedAppendPatternToHoldSpace(content):
    """
    Append the pattern space contents to the hold space with a newline in between.

    Args:
        content (list): The content to process.
    """
    global hold_space
    if hold_space:
        hold_space += '\n' + ''.join(content)
    else:
        hold_space = ''.join(content)
    print("\nHold space updated with appended contents.")

def escape_char(c):
    """
    Escape special characters in a string.

    Args:
        c (str): The character to escape.

    Returns:
        str: The escaped character.
    """
    escape_sequences = {
        '\\': '\\\\', '\a': '\\a', '\b': '\\b', '\f': '\\f',
        '\r': '\\r', '\t': '\\t', '\v': '\\v'
    }
    if c in escape_sequences:
        return escape_sequences[c]
    elif c == '\n':
        return '$\n'
    elif ord(c) < 32 or ord(c) >= 127:
        return f"\\{ord(c):03o}"
    else:
        return c

def sedWritePatternSpace(content):
    """
    Write the pattern space to standard output in an unambiguous form.

    Args:
        content (list): The content to process.
    """
    output = ""
    for line in content:
        escaped_line = "".join(escape_char(c) for c in line.rstrip())
        output += escaped_line + '$\n'
    print("Pattern space written to output in unambiguous form:")
    print(output)

def sedPrintPatternSpace(content):
    """
    Print the entire pattern space to standard output.

    Args:
        content (list): The content to process.
    """
    print("".join(content))

def sedPrintPatternSpaceUpToNewline(content):
    """
    Print the pattern space up to the first newline to standard output.

    Args:
        content (list): The content to process.
    """
    for line in content:
        first_newline_index = line.find('\n')
        if first_newline_index != -1:
            print(line[:first_newline_index])
        else:
            print(line, end='')

def sedPrintLinesMatchingPattern(content, pattern):
    """
    Print lines matching the given pattern to standard output.

    Args:
        content (list): The content to process.
        pattern (str): The pattern to search for.
    """
    matched = False
    pattern_escaped = re.escape(pattern)
    for line in content:
        if re.search(pattern_escaped, line):
            print(line, end='')
            matched = True
    if not matched:
        print(f"\nPattern '{pattern}' not found in the content.")

def print_help():
    """
    Print the help message with the available commands.
    """
    print("\nAvailable commands are:")
    print("'s': 'Substitute - Replace a pattern with a replacement. Expected format: 's/original/replacement/'")
    print("'a': 'Append - Append text after each line matched by a pattern. Expected format: 'a/pattern/newtext/'")
    print("'i': 'Insert - Insert text before each line matched by a pattern. Expected format: 'i/pattern/newtext/'")
    print("'d': 'Delete - Delete lines matching a pattern. Expected format: 'd/word/'")
    print("'g': 'Replace pattern space - Replace pattern space with hold space contents. Expected format: 'g'")
    print("'G': 'Append hold space - Append hold space contents to each line. Expected format: 'G'")
    print("'h': 'Replace hold space - Replace the hold space with the contents of the pattern space. Expected format: 'h'")
    print("'H': 'Append to hold space - Append the pattern space to the hold space with a newline. Expected format: 'H'")
    print("'l': 'Write pattern space - Write the pattern space to standard output in an unambiguous form. Expected format: 'l'")
    print("'p': 'Print - Write the lines matching a pattern to standard output. Expected format: 'p/pattern/'")
    print("'P': 'Print up to first newline - Write the pattern space up to the first newline to standard output. Expected format: 'P'")
    print("'q': 'Quit - Branch to the end of the script and quit. Expected format: 'q'")

def main():
    """
    Main function to execute the script based on command-line arguments.
    """
    if len(sys.argv) < 3:
        print_help()
        return 1

    mode = sys.argv[1]
    command_text = sys.argv[2]
    input_data = sys.argv[3] if len(sys.argv) > 3 else None
    
    commands = command_text.split(';')
    
    if 'L' in commands:
        print_help()
        return 0

    if mode == '-f':
        if input_data and read_file(input_data) is None:
            return 1
        sed_cases(commands, input_data, is_file=True)
    elif mode == '-s':
        if input_data:
            output = sed_cases(commands, input_data, is_file=False)
            if output:
                print(output)
        else:
            print_help()
            return 1
    else:
        print("\nInvalid mode. Use '-f' for file mode or '-s' for string mode.")
        print_help()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
