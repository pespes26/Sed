import sys

# Global hold space
hold_space = []


def sed_cases(commands, file_path):
    content = read_file(file_path)
    if content is None:
        return
    
    substitution_made = False  # Track if a substitution was made

    for command_text in commands:
        if command_text.startswith('s/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 4:
                original = parts[1]
                new = parts[2]
                # Replace the words in the file
                sedSub(file_path, original, new)
                substitution_made = True
            else:
                print("Invalid format for substitution. Expected format: s/original/new/")
                print_help()
                return
        elif command_text.startswith('d/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 3:
                word = parts[1]
                # Delete lines containing the word
                sedDelete(file_path, word)
            else:
                print("Invalid format for deletion. Expected format: d/word/")
                print_help()
                return
        elif command_text.startswith('a/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 4:
                pattern = parts[1]
                newtext = parts[2]
                # Append text after lines containing the pattern
                sedAppend(file_path, pattern, newtext)
            else:
                print("Invalid format for appending. Expected format: a/pattern/newtext/")
                print_help()
                return
        elif command_text.startswith('i/') and command_text.endswith('/'):
            parts = command_text.split('/')
            if len(parts) == 4:
                pattern = parts[1]
                newtext = parts[2]
                # Insert text before lines containing the pattern
                sedInsert(file_path, pattern, newtext)
            else:
                print("Invalid format for inserting. Expected format: i/pattern/newtext/")
                print_help()
                return
        elif command_text == 'g':
            # Replace pattern space with hold space contents
            sedReplacePatternSpace(file_path)
        elif command_text == 'G':
            # Append hold space contents to each line
            sedAppendHoldSpace(file_path)
        elif command_text == 'h':
            # Replace the hold space with the contents of the pattern space
            sedReplaceHoldSpace(file_path)
        elif command_text == 'H':
            # Append the pattern space to the hold space with a newline
            sedAppendPatternToHoldSpace(file_path)
        elif command_text == 'l':
            # Write the pattern space to standard output in an unambiguous form
            sedWritePatternSpace(file_path)
        elif command_text == 'p':
            # Write the pattern space to standard output
            sedPrintPatternSpace(content)
        elif command_text == 'P':
            # Print the pattern space up to the first newline (current content)
            sedPrintPatternSpaceUpToNewline(content)
        elif command_text == "q":
            # Quit and exit from the script
            sys.exit(0)
        elif command_text.startswith('r '):
            # Copy the contents of rfile to standard output
            rfile = command_text.split(' ', 1)[1]
            rfile_content = read_file(rfile)
            if rfile_content:
                print("".join(rfile_content))
            else:
                # rfile does not exist or cannot be read, treated as an empty file
                pass
        elif command_text.startswith('w '):
            # Append the pattern space to wfile
            wfile = command_text.split(' ', 1)[1]
            with open(wfile, 'a') as wf:
                print(f"\nWriting to {wfile}...")
                wf.writelines(content)
        elif command_text.startswith('t'):
            # Test and branch if any substitution was made
            if substitution_made:
                label = command_text[1:].strip()
                if label:
                    if label in commands:
                        index = commands.index(f':{label}')
                        commands = commands[index + 1:]
                        sed_cases(commands, file_path)
                        return
                    else:
                        print(f"Label '{label}' not found.")
                        return
                else:
                    return
        elif command_text.startswith(':'):
            # Label, no action needed
            continue
        elif command_text == 'x':
            # Exchange the contents of the pattern and hold spaces
            sedExchangePatternHold(content)
            print("\nAfter x command, content is:", content)
            print("After x command, hold_space is:", hold_space)
        elif command_text =='L':
            # Printing the command list
            print_help()
        else:
            print("Invalid command.")
            print_help()
            return 1
    return 0


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

def sedSub(file_path, original, new):
    content = read_file(file_path)
    if content is None:
        return
    
    # Show original content
    print(f"\nOriginal content of {file_path}:\n")
    print("".join(content))
    
    # Replace the original string with the new string
    updated_content = [line.replace(original, new) for line in content]
    
    if content == updated_content:
        print("\nNo changes were made to the file.")
    else:
        # Write the updated content back to the file
        write_file(file_path, updated_content)
        # Show modified content
        print(f"\nModified content of {file_path}:\n")
        print("".join(updated_content))
        print(f"\nAll occurrences of '{original}' have been replaced with '{new}' in {file_path}.")

def sedDelete(file_path, word):
    content = read_file(file_path)
    if content is None:
        return
    
    # Show original content
    print(f"\nOriginal content of {file_path}:\n")
    print("".join(content))
    
    # Delete lines containing the word
    updated_content = [line for line in content if word not in line]
    
    if content == updated_content:
        print(f"\nNo lines containing the word '{word}' were found.")
    else:
        # Write the updated content back to the file
        write_file(file_path, updated_content)
        # Show modified content
        print(f"\nModified content of {file_path} (lines containing '{word}' were deleted):\n")
        print("".join(updated_content))

def sedAppend(file_path, pattern, newtext):
    content = read_file(file_path)
    if content is None:
        return
    
    # Show original content
    print(f"\nOriginal content of {file_path}:\n")
    print("".join(content))
    
    # Append newtext after lines containing the pattern
    updated_content = []
    for line in content:
        updated_content.append(line)
        if pattern in line:
            updated_content.append(newtext + '\n')
    
    if content == updated_content:
        print(f"\nNo lines containing the pattern '{pattern}' were found.")
    else:
        # Write the updated content back to the file
        write_file(file_path, updated_content)
        # Show modified content
        print(f"\nModified content of {file_path} (appended '{newtext}' after lines containing '{pattern}'):\n")
        print("".join(updated_content))

def sedInsert(file_path, pattern, newtext):
    content = read_file(file_path)
    if content is None:
        return
    
    # Show original content
    print(f"\nOriginal content of {file_path}:\n")
    print("".join(content))
    
    # Insert newtext before lines containing the pattern
    updated_content = []
    for line in content:
        if pattern in line:
            updated_content.append(newtext + '\n')  # Insert new text
        updated_content.append(line)  # Append the original line
    
    if content == updated_content:
        print(f"\nNo lines containing the pattern '{pattern}' were found.")
    else:
        # Write the updated content back to the file
        write_file(file_path, updated_content)
        # Show modified content
        print(f"\nModified content of {file_path} (inserted '{newtext}' before lines containing '{pattern}'):\n")
        print("".join(updated_content))

def sedAppendHoldSpace(file_path):
    global hold_space
    content = read_file(file_path)
    if content is None:
        return
    
    # Show original content
    print(f"\nOriginal content of {file_path}:\n")
    print("".join(content))
    
    # Append hold space contents to each line with a newline in between
    updated_content = []
    for line in content:
        updated_content.append(line.strip() + '\n' + hold_space + '\n')
    
    # Write the updated content back to the file
    write_file(file_path, updated_content)
    # Show modified content
    print(f"\nModified content of {file_path} (appended hold space contents to each line):\n")
    print("".join(updated_content))

def sedReplaceHoldSpace(file_path):
    global hold_space
    content = read_file(file_path)
    if content is None:
        return
    
    # Replace the hold space with the pattern space (content)
    hold_space = "".join(content)
    print(f"\nHold space updated with the contents of {file_path}.")

def sedReplacePatternSpace(file_path):
    global hold_space
    content = read_file(file_path)
    if content is None:
        return
    
    # Replace the pattern space with the hold space
    updated_content = [hold_space for _ in content]
    
    # Write the updated content back to the file
    write_file(file_path, updated_content)
    # Show modified content
    print(f"\nModified content of {file_path} (replaced pattern space with hold space contents):\n")
    print("".join(updated_content))

def sedAppendPatternToHoldSpace(file_path):

    global hold_space
    content = read_file(file_path)
    if content is None:
        return
    
    # Append pattern space (content) to hold space with a newline in between
    if hold_space:
        hold_space += '\n' + "".join(content)
    else:
        hold_space = "".join(content)
    
    print(f"\nHold space updated with appended contents of {file_path}.")

def escape_char(c):
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

def sedWritePatternSpace(file_path):
    content = read_file(file_path)
    if content is None:
        return

    output = ""
    for line in content:
        escaped_line = "".join(escape_char(c) for c in line.rstrip())
        output += escaped_line + '$\n'

    print("Pattern space written to output in unambiguous form:")
    print(output)

def sedNextLine(file_path, current_line_index):
    content = read_file(file_path)
    if content is None:
        return None, current_line_index
    
    # Write the current pattern space to standard output if not suppressed
    if not suppress_output:
        print(content[current_line_index], end='')

    # Move to the next line
    next_line_index = current_line_index + 1
    if next_line_index >= len(content):
        return None, next_line_index  # No more lines

    # Return the next line content and updated line index
    next_line = content[next_line_index].rstrip()
    return next_line, next_line_index    

def sedPrintPatternSpace(file_path):

    content = read_file(file_path)
    if content is None:
        return

    for line in content:
        print(line, end='')
        
def sedPrintPatternSpaceUpToNewline(content):
    for line in content:
        print(line.split('\\n')[0])  # Print up to the first newline   
        
def sedExchangePatternHold(content):
    global hold_space
    # Exchange the contents of the pattern space and hold space
    temp = content.copy()
    content.clear()
    content.extend(hold_space)
    hold_space = temp
    
def print_help():
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
    print("'p': 'Print - Write the entire pattern space to standard output. Expected format: 'p'")
    print("'P': 'Print up to newline - Write the pattern space up to the first newline to standard output. Expected format: 'P'")
    print("'q': 'Quit - Branch to the end of the script and quit. Expected format: 'q'")
    print("'t': 'Test - Branch to the : command verb bearing the label if any substitutions have been made. Expected format: 't[label]'")
    print("'w': 'Write - Append the pattern space to wfile. Expected format: 'w wfile'")
    print("'x': 'Exchange - Exchange the contents of the pattern space and hold space. Expected format: 'x'")
    print("'L': 'List - List all available commands. Expected format: 'L'")

def main():
    if len(sys.argv) < 3:
        print_help()
        return 1

    # Get the command-line arguments
    command_text = sys.argv[1]
    file_path = sys.argv[2]
    
    # Split the commands by semicolons
    commands = command_text.split(';')
    
        # Check if the file exists
        # Check if the file exists
    if read_file(file_path) is None:
        return 1
        
    sed_cases(commands,file_path)
    
    
    # Validate the command and format

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
