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
@click.option('-e', multiple=True, help='Add the script of editing commands to the end of the script')
@click.option('-f', type=click.File('r'), multiple=True, help='Add the editing commands in the file script_file to the end of the script')
@click.argument('files', nargs=-1, type=click.Path(exists=True))
def main(e, f, files):
    """
    A simple sed-like utility that uses regular expressions to substitute text.
    
    \b
    Usage examples:
    - Substitute "old" with "new" in a file:
      python sed.py -e "s/old/new/" sample.txt
    
    - Delete lines containing "remove":
      python sed.py -e "d/remove/" sample.txt
    
    - Insert "Inserted text" before lines containing "match":
      echo "Line to match" | python sed.py -e "i/match/Inserted text"
    
    - Append "additional text" after lines containing "append":
      python sed.py -e "a/append/additional text/" sample.txt
    
    - Print lines containing "pattern":
      python sed.py -e "p/pattern/" sample.txt
    
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
                    result = process_sed(full_script, file, is_file=True)
                    write_file(file, result.splitlines(keepends=True))
                except Exception as err:
                    click.echo(f"\nAn error occurred while processing the file '{file}': {err}", err=True)
                    sys.exit(ERROR_PROCESSING_FILE)
        elif not sys.stdin.isatty():
            input_data = sys.stdin.read()
            if not input_data.strip():
                click.echo("Error: No input provided from stdin.", err=True)
                sys.exit(ERROR_NO_COMMANDS)
            try:
                result = process_sed(full_script, input_data, is_file=False)
                click.echo(result, nl=False)
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

def process_sed(commands, input_data, is_file=True):
    """
    Process a series of sed-like commands on given input data.
    
    Args:
        commands (str): The commands to execute.
        input_data (str): The path to the file or the input string to process.
        is_file (bool): Flag indicating whether input_data is a file path or a direct string.
    
    Returns:
        str: The processed string with the applied commands.
    """
    try:
        if is_file:
            content = read_file(input_data)
        else:
            content = input_data.splitlines(keepends=True)

        if content is None:
            sys.exit(ERROR_READING_FILE)

        result = []
        for cmd in commands.split(';'):
            cmd = cmd.strip()
            if not cmd:
                continue
            try:
                if re.match(r'^s/.*/.*/$', cmd):
                    original, new = cmd.split('/')[1:3]
                    if any(re.search(original, line) for line in content):
                        click.echo(f"\nReplacing {original} with {new}")
                        content = [re.sub(original, new, line) for line in content]
                    else:
                        click.echo(f"\n'{original}' not found")
                elif re.match(r'^d/.*/$', cmd):
                    pattern = cmd.split('/')[1]
                    if any(re.search(pattern, line) for line in content):
                        click.echo(f"\nDeleting {pattern} from matched lines.")
                        content = [line for line in content if not re.search(pattern, line)]
                    else:
                        click.echo(f"\n'{pattern}' not found")
                elif re.match(r'^a/.*/.*/$', cmd):
                    pattern, newtext = cmd.split('/')[1:3]
                    new_content = []
                    if any(re.search(pattern, line) for line in content):
                        click.echo(f"\nAppending {newtext} after matched lines.")
                        for line in content:
                            new_content.append(line)
                            if re.search(pattern, line):
                                new_content.append(newtext + '\n')
                        content = new_content
                    else:
                        click.echo(f"\n{pattern} not found.")
                elif re.match(r'^i/.*/.*/$', cmd):
                    pattern, newtext = cmd.split('/')[1:3]
                    new_content = []
                    if any(re.search(pattern, line) for line in content):
                        click.echo(f"\Insert {newtext} before matched lines.")
                        for line in content:
                            if re.search(pattern, line):
                                new_content.append(newtext + '\n')
                            new_content.append(line)
                        content = new_content
                    else:
                        click.echo(f"\n{pattern} not found.")
                elif re.match(r'^p/.*/$', cmd):
                    pattern = cmd.split('/')[1]
                    matched_lines = [line for line in content if re.search(pattern, line)]
                    if matched_lines:
                        result = "".join(matched_lines)
                        click.echo(f"\nMatched lines:\n{result}")
                        return "".join(matched_lines)
                    else:
                        click.echo(f"\n'{pattern}' not found")
                else:
                    click.echo("\nInvalid command.", err=True)
                    sys.exit(ERROR_INVALID_FORMAT)
            except Exception as err:
                click.echo(f"\nAn error occurred while processing command '{cmd}': {err}", err=True)
                sys.exit(ERROR_PROCESSING_FILE)

        if result:
            click.echo("\n"+"".join(result))
            return "".join(result)
        else:
            click.echo("\n"+"".join(content))
            return "".join(content)

    except Exception as err:
        click.echo(f"\nAn error occurred while processing sed commands: {err}", err=True)
        sys.exit(ERROR_PROCESSING_FILE)

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
            return [line if line.endswith('\n') else line + '\n' for line in file.readlines()]
    except FileNotFoundError:
        click.echo(f"The file '{file_path}' does not exist.", err=True)
        sys.exit(ERROR_FILE_NOT_FOUND)
    except Exception as e:
        click.echo(f"An error occurred: {e}", err=True)
        sys.exit(ERROR_READING_FILE)

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
        click.echo(f"An error occurred: {e}", err=True)
        sys.exit(ERROR_WRITING_FILE)

if __name__ == "__main__":
    main()
