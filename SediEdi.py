import argparse
import re
import sys

def apply_command(command, pattern, replacement_or_text, text, line_number=None):
    if line_number:
        return apply_command_to_line(command, pattern, replacement_or_text, text, line_number)
    if command == 's':
        if not re.search(pattern, text):
            print(f"Pattern '{pattern}' not found in the text.")
            return None
        return replace_in_text(pattern, replacement_or_text, text)
    elif command == 'a':
        return append_text(pattern, replacement_or_text, text)
    elif command == 'i':
        return insert_text(pattern, replacement_or_text, text)
    elif command == 'd':
        if not re.search(pattern, text):
            print(f"Pattern '{pattern}' not found in the text.")
            return None
        return delete_lines(pattern, text)
    elif command == 'p':
        return print_lines(pattern, text)
    elif command == 'n':
        return get_next_line(pattern, text)
    else:
        print(f"Unsupported command: {command}")
        return text

def apply_command_to_line(command, pattern, replacement_or_text, text, line_number):
    lines = text.splitlines()
    if isinstance(line_number, tuple):
        start_line, end_line = line_number
        if start_line < 1 or end_line > len(lines) or start_line > end_line:
            print(f"Invalid line range: {start_line},{end_line}")
            return text
        for i in range(start_line - 1, end_line):
            lines[i] = apply_command(command, pattern, replacement_or_text, lines[i], None)
        return '\n'.join(lines) + '\n'
    else:
        if line_number < 1 or line_number > len(lines):
            print(f"Invalid line number: {line_number}")
            return text

        target_line = lines[line_number - 1]
        if command == 's':
            if not re.search(pattern, target_line):
                print(f"Pattern '{pattern}' not found in the specified line.")
                return text
            lines[line_number - 1] = re.sub(pattern, replacement_or_text, target_line)
        elif command == 'a':
            if re.search(pattern, target_line):
                lines.insert(line_number, replacement_or_text)
        elif command == 'i':
            if re.search(pattern, target_line):
                lines.insert(line_number - 1, replacement_or_text)
        elif command == 'd':
            if re.search(pattern, target_line):
                lines.pop(line_number - 1)
        elif command == 'p':
            if re.search(pattern, target_line):
                print(target_line)
        elif command == 'n':
            if re.search(pattern, target_line):
                return get_next_line(pattern, text)
        else:
            print(f"Unsupported command: {command}")
            return text

    return '\n'.join(lines) + '\n'

def replace_in_text(pattern, replacement, text):
    return re.sub(pattern, replacement, text)

def append_text(pattern, append_text, text):
    lines = text.splitlines()
    result = []
    for line in lines:
        result.append(line)
        if re.search(pattern, line):
            result.append(append_text)
    return '\n'.join(result) + '\n'

def insert_text(pattern, insert_text, text):
    lines = text.splitlines()
    result = []
    for line in lines:
        if re.search(pattern, line):
            result.append(insert_text)
        result.append(line)
    return '\n'.join(result) + '\n'

def delete_lines(pattern, text):
    lines = text.splitlines()
    result = [line for line in lines if not re.search(pattern, line)]
    return '\n'.join(result) + '\n'

def print_lines(pattern, text):
    lines = text.splitlines()
    result = [line for line in lines if re.search(pattern, line)]
    for line in result:
        print(line)
    return '\n'.join(result) + '\n'

def get_next_line(pattern, text):
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.search(pattern, line):
            if i + 1 < len(lines):
                return lines[i + 1]
            else:
                return ""
    return ""

def write_content(new_content, file_path):
    try:
        with open(file_path, 'w') as file:
            file.write(new_content)
        print(f"Wrote new content to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def read_files_or_stdin(files):
    if files and files[0] != '-':
        content = ''
        for file_path in files:
            try:
                with open(file_path, 'r') as file:
                    file_content = file.read()
                    if not file_content.strip():  # Check if the file is empty
                        print(f"The file '{file_path}' is empty.")
                    content += file_content + '\n'
            except FileNotFoundError:
                print(f"File not found: {file_path}")
        return content
    else:
        stdin_content = sys.stdin.read()
        if not stdin_content.strip():  # Check if stdin content is empty
            print("No input received from stdin.")
            return None
        return stdin_content

def list_commands():
    commands = {
        's': 'Substitute - Replace a pattern with a replacement',
        'a': 'Append - Append text after each line matched by a pattern',
        'i': 'Insert - Insert text before each line matched by a pattern',
        'd': 'Delete - Delete lines matching a pattern',
        'p': 'Print - Print lines matching a pattern',
        'n': 'Next - Get the next line matching a pattern',
        'w': 'Write - Write new content to the file',
        'l': 'List - List all available commands'
    }
    print("Available commands:")
    for cmd, desc in commands.items():
        print(f"{cmd}: {desc}")

def parse_script_argument(script_arg):
    if script_arg == 'l//':
        return 'l', None, None, None

    address_pattern = r'(\d*,?\d*)?([sadiwpnl])/([^/]+)/(.+)?/?$'
    match = re.match(address_pattern, script_arg)
    if not match:
        print("Invalid script format. Use '[address[,address]]command/pattern/replacement/'")
        sys.exit(1)

    addresses, command, pattern, replacement_or_text = match.groups()

    if addresses:
        address_list = addresses.split(',')
        if len(address_list) == 1:
            line_number = int(address_list[0])
        elif len(address_list) == 2:
            start_line = int(address_list[0])
            end_line = int(address_list[1])
            line_number = (start_line, end_line)
        else:
            print("Invalid address format. Use '[address[,address]]'")
            sys.exit(1)
    else:
        line_number = None

    if replacement_or_text and replacement_or_text.endswith('/'):
        replacement_or_text = replacement_or_text[:-1]

    # For 'w' command, pattern is actually the text to write
    if command == 'w':
        replacement_or_text = pattern
        pattern = None

    return command, pattern, replacement_or_text, line_number

def read_script_files(script_files):
    scripts = []
    for script_file in script_files:
        try:
            with open(script_file, 'r') as file:
                scripts.extend(file.readlines())
        except FileNotFoundError:
            print(f"Script file not found: {script_file}")
    return scripts

def main():
    parser = argparse.ArgumentParser(description="A limited version of sed implemented in Python.")
    parser.add_argument('-n', action='store_true', help="Suppress automatic printing of pattern space.")
    parser.add_argument('-e', action='append', help="Add the script to the commands to be executed.")
    parser.add_argument('-f', action='append', help="Add the script file to the commands to be executed.")
    parser.add_argument('script', nargs='?', help="The sed script in the format '[address[,address]]command/pattern/replacement/'")
    parser.add_argument('files', help="The files to process", nargs='*')

    args = parser.parse_args()

    scripts = []

    if args.script:
        scripts.append(args.script.strip("'"))
    if args.e:
        scripts.extend(args.e)
    if args.f:
        scripts.extend(read_script_files(args.f))

    if not scripts:
        print("No scripts provided. Use -e or -f options or provide a script argument.")
        return

    for script in scripts:
        command, pattern, replacement_or_text, line_number = parse_script_argument(script)
        if command == 'l':
            list_commands()
            return

    content = read_files_or_stdin(args.files)
    if content is None:
        print("No content to process.")
        return

    for script in scripts:
        command, pattern, replacement_or_text, line_number = parse_script_argument(script)
        output_file = args.files[0] if args.files and args.files[0] != '-' else None
        content = apply_command(command, pattern, replacement_or_text, content, line_number)

        if not args.n and command != 'w' and command != 'l':
            print(content)

    if command == 'w':
        write_content(replacement_or_text, output_file)

if __name__ == "__main__":
    main()
