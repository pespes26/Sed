# BasicSed.py

A simple script to perform basic `sed`-like text manipulations on files or strings using Python.

## Description

`BasicSed.py` allows you to perform text substitutions, deletions, insertions, and other manipulations on text files or strings. The script supports multiple commands and provides feedback after each command is executed.

## Commands

- `s/original/new/` - Substitute the original text with the new text.
- `d/pattern/` - Delete lines containing the pattern.
- `a/pattern/newtext/` - Append newtext after lines containing the pattern.
- `i/pattern/newtext/` - Insert newtext before lines containing the pattern.
- `p/pattern/` - Print lines matching the pattern.
- `g` - Replace pattern space with hold space contents.
- `G` - Append hold space contents to each line.
- `h` - Replace the hold space with the pattern space contents.
- `H` - Append the pattern space to the hold space with a newline.
- `l` - Write the pattern space to standard output in an unambiguous form.
- `P` - Print all the content
- `q` - Quit the script.

## Usage

### File Mode

To perform operations on a file, use the `-f` flag followed by the commands and the file name.

```bash
python BasicSed.py -f "command1;command2;..." filename
```

### Examples

- **Substitute (`s`)**: replace "brown" with "green" in example.txt:

  ```sh
  python BasicSed.py -f "s/brown/green/" example.txt
  ```

- **Append (`a`)**: Append text after each line matched by a pattern:

  ```sh
  python BasicSedSed.py "a/sample/append this text/" example.txt
  ```

- **Insert (`i`)**: Insert text before each line matched by a pattern on all lines:

  ```sh
  python BasicSedSed.py "i/sample/insert this text/" example.txt
  ```

- **Delete (`d`)**: Delete lines matching a pattern on lines:

  ```sh
  python BasicSed.py -f "d/data/" example.txt
  ```
  
- **Print ('p')**: Print lines containing "All" in example.txt:
  ```sh
  python BasicSed.py -f "p/All/" example.txt
  ```
- **Print all the content ('P')**:
  ```sh
  python BasicSed.py -f "P" example.txt
  ```
- **Combine multiple commands in example.txt***:
  ```sh
  python BasicSed.py -f "s/brown/green/;d/data/;p/All/" example.txt
  ```

  
### String Mode

To perform operations on a direct string input, use the -s flag followed by the commands and the string.
```bash
python BasicSed.py -s "command1;command2;..." "your input string"
```
Instead enter the file name , you should enter the string.

### Output

For each command, the script provides feedback:
- If the pattern is found, it prints the relevant lines.
- If the pattern is not found, it prints a proper message.
- After all commands are executed, it prints the final content.

### Help
To display the help message with the available commands:
```bash
python BasicSed.py -f "L"
```
To activate the venv:
```bash
cd to the script path
venv\Scripts\activate
```



