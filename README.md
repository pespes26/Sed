# SedIntel

A limited version of the `sed` utility implemented in Python, supporting basic text editing commands with addresses.

## Features

- Substitute text patterns
- Append text after matching lines
- Insert text before matching lines
- Delete lines containing specific patterns
- Print lines matching a pattern
- Get the next line matching a pattern
- Write new content to files
- List all available commands
- Error handling and exit codes

## Usage

```bash
python Sed.py "<commands>" <file>
```

### Commands

#### Address Types

- `[0addr]`: Zero addresses
- `[1addr]`: One address
- `[2addr]`: Two addresses

#### Editing Commands

- **Editing Commands**:
  - `s/pattern/replacement/` - Substitute `pattern` with `replacement`.
  - `a/pattern/append text/` - Append `append text` after each line matched by `pattern`.
  - `i/pattern/insert text/` - Insert `insert text` before each line matched by `pattern`.
  - `d/pattern/` - Delete lines matching `pattern`.
  - `p/pattern/` - Print lines matching pattern.
  - `n/pattern/` - Get the next line matching pattern.
  - `w//new content/` - Write `new content` to the specified file.
  - `l//` - List all available commands.


1. **[2addr] `{ editing command }`**

   - Execute a list of `sed` editing commands only when the pattern space is selected.

2. **[1addr] `a\`**

   - `text`: Write text to standard output.

3. **[2addr] `b [label]`**

   - Branch to the `:` command verb bearing the label argument. If the label is not specified, branch to the end of the script.

4. **[2addr] `c\`**

   - `text`: Delete the pattern space. Place text on the output and start the next cycle.

5. **[2addr] `d`**

   - Delete the pattern space and start the next cycle.

6. **[2addr] `D`**

   - If the pattern space contains no `<newline>`, delete the pattern space and start a normal new cycle as if the `d` command was issued. Otherwise, delete the initial segment of the pattern space through the first `<newline>`, and start the next cycle with the resultant pattern space and without reading any new input.

7. **[2addr] `g`**

   - Replace the contents of the pattern space by the contents of the hold space.

8. **[2addr] `G`**

   - Append to the pattern space a `<newline>` followed by the contents of the hold space.

9. **[2addr] `h`**

   - Replace the contents of the hold space with the contents of the pattern space.

10. **[2addr] `H`**

    - Append to the hold space a `<newline>` followed by the contents of the pattern space.

11. **[1addr] `i\`**

    - `text`: Write text to standard output.

12. **[2addr] `l`**

    - Write the pattern space to standard output in a visually unambiguous form.

13. **[2addr] `n`**

    - Write the pattern space to standard output if the default output has not been suppressed, and replace the pattern space with the next line of input, less its terminating `<newline>`.

14. **[2addr] `N`**

    - Append the next line of input, less its terminating `<newline>`, to the pattern space, using an embedded `<newline>` to separate the appended material from the original material.

15. **[2addr] `p`**

    - Write the pattern space to standard output.

16. **[2addr] `P`**

    - Write the pattern space, up to the first `<newline>`, to standard output.

17. **[1addr] `q`**

    - Branch to the end of the script and quit without starting a new cycle.

18. **[1addr] `r rfile`**

    - Copy the contents of `rfile` to standard output as described previously.

19. **[2addr] `s/BRE/replacement/flags`**

    - Substitute the replacement string for instances of the BRE in the pattern space.

20. **[2addr] `t [label]`**

    - Branch to the `:` command verb bearing the label if any substitutions have been made since the most recent reading of an input line or execution of a `t`.

21. **[2addr] `w wfile`**

    - Append (write) the pattern space to `wfile`.

22. **[2addr] `x`**

    - Exchange the contents of the pattern and hold spaces.

23. **[2addr] `y/string1/string2/`**

    - Replace all occurrences of characters in `string1` with the corresponding characters in `string2`.

24. **[0addr] `:label`**

    - Do nothing. This command bears a label to which the `b` and `t` commands branch.

25. **[1addr] `=`**

    - Write the current line number to standard output.

26. **[0addr]**

    - Ignore this empty command.

27. **[0addr] `#`**
    - Ignore the `#` and the remainder of the line (treat them as a comment).

- **List Available Commands**:

  ```sh
  python SediEdi.py 'L' 
  ```

- **Write New Content**: Write "new content" to `sample.txt`:

  ```sh
  python SediEdi.py 'w//new content/' sample.txt
  ```

- **Substitute (`s`)**: Replace a pattern with a replacement on lines 1 to 5:

  ```sh
  python SediEdi.py '1,5s/on/forward/' sample.txt
  ```

- **Append (`a`)**: Append text after each line matched by a pattern on lines 1 to 10:

  ```sh
  python SediEdi.py '1,10a/sample/append this text/' sample.txt
  ```

- **Insert (`i`)**: Insert text before each line matched by a pattern on all lines:

  ```sh
  python SediEdi.py 'i/sample/insert this text/' sample.txt
  ```

- **Delete (`d`)**: Delete lines matching a pattern on lines 3 to 7:

  ```sh
  python SediEdi.py '3,7d/sample/' sample.txt
  ```
  
- **Print ('p')**: Print lines matching "sample":
  ```sh
  python SediEdi.py 'p/sample/' sample.txt
  ```
 
- **Next Line ('n')**:  Get the next line after the one matching "sample":
  ```sh
  python SediEdi.py 'n/sample/' sample.txt
  ```
```

### Exit Values

- `0`: Successful completion.
- `>0`: An error occurred.
