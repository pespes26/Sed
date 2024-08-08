import sys
import click
import re

# Error codes
ERROR_NO_COMMANDS = 1
ERROR_FILE_NOT_FOUND = 2
ERROR_INVALID_FORMAT = 3
ERROR_PROCESSING_FILE = 4
ERROR_READING_FILE = 5
ERROR_WRITING_FILE = 6
ERROR_UNKNOWN = 7

@click.command()
@click.option('-n', is_flag=True, help='Suppress automatic printing of pattern space')
@click.option('-e', multiple=True, help='Add the script of editing commands to the end of the script')
@click.option('-f', type=click.File('r'), multiple=True, help='Add the editing commands in the file script_file to the end of the script')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def main(n, e, f, files):
    """
    A simple sed-like utility that uses regular expressions to substitute text.

    Example Usage:
    - Substitute "Python" with "Java" in a file:
      python sed.py -e "s/Python/Java/" sample.txt
    
    - Delete lines containing "remove":
      python sed.py -e "d/remove/" sample.txt
    
    - Insert "Inserted text" before lines containing "match":
      echo "Line to match" | python sed.py -e "i/match/Inserted text"
    
    - Append "additional text" after lines containing "append":
      python sed.py -e "a/append/additional text/" sample.txt
    
    - Print lines containing "quick":
      python sed.py -n -e "p/quick/" sample.txt
    
    Multiple commands can be combined using the `-e` option multiple times or using a script file with the `-f` option.
    """
    try:
        scripts = [script for script in e if script.strip()] + [line for file in f for line in file.read().splitlines()]

        if not scripts:
            click.echo("No commands provided.", err=True)
            sys.exit(ERROR_NO_COMMANDS)

        full_script = "\n".join(scripts)

        if files:
            for file in files:
                try:
                    process_sed(full_script, file, suppress_output=n, is_file=True)
                except Exception as err:
                    click.echo(f"\nAn error occurred while processing the file '{file}': {err}", err=True)
                    sys.exit(ERROR_PROCESSING_FILE)
        elif not sys.stdin.isatty():
            input_data = sys.stdin.read()
            if not input_data.strip():
                click.echo("Error: No input provided from stdin.", err=True)
                sys.exit(ERROR_NO_COMMANDS)
            try:
                output = process_sed(full_script, input_data, suppress_output=n, is_file=False)
                if output:
                    click.echo(output, nl=False)
            except Exception as err:
                click.echo(f"\nAn error occurred while processing stdin input: {err}", err=True)
                sys.exit(ERROR_PROCESSING_FILE)
        else:
            click.echo("Error: No files provided and no input from stdin.", err=True)
            sys.exit(ERROR_NO_COMMANDS)

        sys.exit(0)
    except Exception as err:
        click.echo(f"\nAn unknown error occurred: {err}", err=True)
        sys.exit(ERROR_UNKNOWN)

def process_sed(commands, input_data, suppress_output=False, is_file=True):
    """
    Process a series of sed-like commands on given input data.

    Args:
        commands (str): The commands to execute.
        input_data (str): The path to the file or the input string to process.
        suppress_output (bool): Flag to suppress automatic printing of pattern space.
        is_file (bool): Flag indicating whether input_data is a file path or a direct string.

    Returns:
        None if is_file is True.
        str if is_file is False, representing the processed string.
    """
    try:
        content = read_file(input_data) if is_file else input_data.splitlines(keepends=True)

        if content is None:
            sys.exit(ERROR_READING_FILE)

        result = []
        for cmd in commands.split(';'):
            try:
                if re.match(r'^s/.*/.*/g$', cmd):
                    original, new = cmd.split('/')[1:3]
                    if any(re.search(original, line) for line in content):
                        click.echo(f"\nReplacing '{original}' with '{new}' globally")
                        content = [re.sub(original, new, line) for line in content]
                    else:
                        click.echo(f"\n'{original}' not found")
                elif re.match(r'^d/.*/$', cmd):
                    pattern = cmd.split('/')[1]
                    if any(re.search(pattern, line) for line in content):
                        click.echo(f"\nDeleting lines containing '{pattern}'")
                        content = [line for line in content if not re.search(pattern, line)]
                    else:
                        click.echo(f"\n'{pattern}' not found")
                elif re.match(r'^a/.*/.*/$', cmd):
                    pattern, newtext = cmd.split('/')[1:3]
                    if any(re.search(pattern, line) for line in content):
                        click.echo(f"\nAppending '{newtext}' after lines containing '{pattern}'")
                        content = [line + newtext + '\n' if re.search(pattern, line) else line for line in content]
                    else:
                        click.echo(f"\n'{pattern}' not found")
                elif re.match(r'^i/.*/.*/$', cmd):
                    pattern, newtext = cmd.split('/')[1:3]
                    if any(re.search(pattern, line) for line in content):
                        click.echo(f"\nInserting '{newtext}' before lines containing '{pattern}'")
                        content = [newtext + '\n' + line if re.search(pattern, line) else line for line in content]
                    else:
                        click.echo(f"\n'{pattern}' not found")
                elif re.match(r'^p/.*/$', cmd):
                    pattern = cmd.split('/')[1]
                    matched_lines = [line for line in content if re.search(pattern, line)]
                    if matched_lines:
                        click.echo(f"\nPrinting lines matching '{pattern}'")
                        if suppress_output:
                            result.extend(matched_lines)
                        else:
                            for line in matched_lines:
                                click.echo(f"{line}", nl=False)
                    else:
                        click.echo(f"\n'{pattern}' not found")
                else:
                    click.echo("\nInvalid command.", err=True)
                    sys.exit(ERROR_INVALID_FORMAT)
            except Exception as err:
                click.echo(f"\nAn error occurred while processing command '{cmd}': {err}", err=True)
                sys.exit(ERROR_PROCESSING_FILE)

        if suppress_output:
            return "".join(result)

        if is_file and input_data:
            write_file(input_data, content)
        else:
            return "".join(content)

        if not suppress_output:
            click.echo("\nContent:")
            click.echo("".join(content))

    except Exception as err:
        click.echo(f"\nAn error occurred while processing sed commands: {err}", err=True)
        sys.exit(ERROR_PROCESSING_FILE)

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        click.echo(f"\nThe file '{file_path}' does not exist.", err=True)
        sys.exit(ERROR_FILE_NOT_FOUND)
    except Exception as e:
        click.echo(f"\nAn error occurred: {e}", err=True)
        sys.exit(ERROR_READING_FILE)

def write_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.writelines(content)
    except Exception as e:
        click.echo(f"\nAn error occurred: {e}", err=True)
        sys.exit(ERROR_WRITING_FILE)

if __name__ == "__main__":
    main()
