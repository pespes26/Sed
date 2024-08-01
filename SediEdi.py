import argparse
import re
import sys


def apply_command(command, pattern, replacement_or_text, text, start_addr, end_addr):
    if command == 's':
        return replace_in_text(pattern, replacement_or_text, text, start_addr, end_addr)
    elif command == 'a':
        return append_text(pattern, replacement_or_text, text, start_addr, end_addr)
    elif command == 'i':
        return insert_text(pattern, replacement_or_text, text, start_addr, end_addr)
    elif command == 'd':
        return delete_lines(pattern, text, start_addr, end_addr)
    else:
        print(f"Unsupported command: {command}")
        return text


def replace_in_text(pattern, replacement, text, start_addr, end_addr):
    return apply_on_range(lambda line: re.sub(pattern, replacement, line), text, start_addr, end_addr)


def append_text(pattern, append_text, text, start_addr, end_addr):
    def append_if_match(line):
        return line + '\n' + append_text if re.search(pattern, line) else line

    return apply_on_range(append_if_match, text, start_addr, end_addr)


def insert_text(pattern, insert_text, text, start_addr, end_addr):
    def insert_if_match(line):
        return insert_text + '\n' + line if re.search(pattern, line) else line

    return apply_on_range(insert_if_match, text, start_addr, end_addr)


def delete_lines(pattern, text, start_addr, end_addr):
    return apply_on_range(lambda line: None if re.search(pattern, line) else line, text, start_addr, end_addr,
                          keep_none=False)


def apply_on_range(func, text, start_addr, end_addr, keep_none=True):
    lines = text.splitlines()
    result = []
    for i, line in enumerate(lines, 1):
        if start_addr <= i <= end_addr:
            processed_line = func(line)
            if processed_line is not None or keep_none:
                result.append(processed_line)
        else:
            result.append(line)
    return '\n'.join(result) + '\n'


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
            with open(file_path, 'r') as file:
                content += file.read() + '\n'
        return content
    else:
        return sys.stdin.read()


def list_commands():
    commands = {
        's': 'Substitute - Replace a pattern with a replacement',
        'a': 'Append - Append text after each line matched by a pattern',
        'i': 'Insert - Insert text before each line matched by a pattern',
        'd': 'Delete - Delete lines matching a pattern',
        'w': 'Write - Write new content to the file',
        'l': 'List - List all available commands'
    }
    print("Available commands:")
    for cmd, desc in commands.items():
        print(f"{cmd}: {desc}")


def parse_addresses(addr_string):
    if not addr_string:
        return 1, float('inf')
    addrs = addr_string.split(',')
    start_addr = int(addrs[0]) if addrs[0].isdigit() else 1
    end_addr = int(addrs[1]) if len(addrs) > 1 and addrs[1].isdigit() else float('inf')
    return start_addr, end_addr


def process_file(command, pattern, replacement_or_text, content, start_addr, end_addr, output_file=None):
    try:
        if command == 'w':
            write_content(replacement_or_text, output_file)
            return

        print(f"Original content:\n{content}\n")  # Debugging output

        modified_content = apply_command(command, pattern, replacement_or_text, content, start_addr, end_addr)

        print(f"Modified content:\n{modified_content}\n")  # Debugging output

        if output_file:
            with open(output_file, 'w') as file:
                file.write(modified_content)
        else:
            sys.stdout.write(modified_content)

        print(f"Processed '{command}' with pattern '{pattern}'")
    except Exception as e:
        print(f"Error processing content: {e}")


def main():
    print("Starting script...")  # Debugging output

    parser = argparse.ArgumentParser(description="A limited version of sed implemented in Python.")
    parser.add_argument('script',
                        help="The sed script in the format '[address[,address]]command/pattern/replacement_or_text/'")
    parser.add_argument('files', help="The files to process", nargs='*')

    args = parser.parse_args()

    print(f"Arguments received: script={args.script}, files={args.files}")  # Debugging output

    # Extract the address, command, pattern, and replacement or text from the script argument
    script_match = re.match(r'(\d*,?\d*)?([sadiwl])/([^/]*)/([^/]*)/?', args.script)
    if not script_match:
        print("Invalid script format. Use '[address[,address]]command/pattern/replacement_or_text/'")
        return

    addr_string = script_match.group(1)
    command = script_match.group(2)
    pattern = script_match.group(3)
    replacement_or_text = script_match.group(4) if len(script_match.groups()) > 3 else ''

    start_addr, end_addr = parse_addresses(addr_string)

    print(
        f"Command: '{command}', Pattern: '{pattern}', Replacement/Text: '{replacement_or_text}', Start Addr: {start_addr}, End Addr: {end_addr}")  # Debugging output

    if command == 'l':
        list_commands()
    else:
        content = read_files_or_stdin(args.files)
        output_file = args.files[0] if args.files and args.files[0] != '-' else None
        process_file(command, pattern, replacement_or_text, content, start_addr, end_addr, output_file)


if __name__ == "__main__":
    main()
