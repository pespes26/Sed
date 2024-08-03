import sys

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
        return content
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
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

def replace_in_file(file_path, original, new):
    content = read_file(file_path)
    if content is None:
        return
    
    # Show original content
    print(f"Original content of {file_path}:\n")
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

def delete_lines_with_word(file_path, word):
    content = read_file(file_path)
    if content is None:
        return
    
    # Show original content
    print(f"Original content of {file_path}:\n")
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

def append_text_after_pattern(file_path, pattern, newtext):
    content = read_file(file_path)
    if content is None:
        return
    
    # Show original content
    print(f"Original content of {file_path}:\n")
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

def insert_text_before_pattern(file_path, pattern, newtext):
    content = read_file(file_path)
    if content is None:
        return
    
    # Show original content
    print(f"Original content of {file_path}:\n")
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

def print_help():
    print("Invalid command. Available commands are:")
    print("'s': 'Substitute - Replace a pattern with a replacement'")
    print("'a': 'Append - Append text after each line matched by a pattern'")
    print("'i': 'Insert - Insert text before each line matched by a pattern'")
    print("'d': 'Delete - Delete lines matching a pattern'")
    print("'p': 'Print - Print lines matching a pattern'")
    print("'n': 'Next - Get the next line matching a pattern'")
    print("'w': 'Write - Write new content to the file'")
    print("'l': 'List - List all available commands'")

def main():
    if len(sys.argv) != 3:
        print_help()
        return

    # Get the command-line arguments
    command_text = sys.argv[1]
    file_path = sys.argv[2]
    
    # Split the argument
    if command_text.startswith('s/') and command_text.endswith('/'):
        parts = command_text.split('/')
        if len(parts) == 4:
            original = parts[1]
            new = parts[2]
            # Replace the words in the file
            replace_in_file(file_path, original, new)
        else:
            print("Invalid format for substitution. Expected format: s/original/new/")
            print_help()
    elif command_text.startswith('d/') and command_text.endswith('/'):
        parts = command_text.split('/')
        if len(parts) == 3:
            word = parts[1]
            # Delete lines containing the word
            delete_lines_with_word(file_path, word)
        else:
            print("Invalid format for deletion. Expected format: d/word/")
            print_help()
    elif command_text.startswith('a/') and command_text.endswith('/'):
        parts = command_text.split('/')
        if len(parts) == 4:
            pattern = parts[1]
            newtext = parts[2]
            # Append text after lines containing the pattern
            append_text_after_pattern(file_path, pattern, newtext)
        else:
            print("Invalid format for appending. Expected format: a/pattern/newtext/")
            print_help()
    elif command_text.startswith('i/') and command_text.endswith('/'):
        parts = command_text.split('/')
        if len(parts) == 4:
            pattern = parts[1]
            newtext = parts[2]
            # Insert text before lines containing the pattern
            insert_text_before_pattern(file_path, pattern, newtext)
        else:
            print("Invalid format for inserting. Expected format: i/pattern/newtext/")
            print_help()
    else:
        print("Invalid command format.")
        print_help()

if __name__ == "__main__":
    main()
