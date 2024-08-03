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

#### Exit Values

- `0`: Successful completion.
- `>0`: An error occurred.
  
#### Editing Commands

- **Editing Commands**:
  - `s/pattern/replacement/` - Substitute `pattern` with `replacement`.
  - `a/pattern/append text/` - Append `append text` after each line matched by `pattern`.
  - `i/pattern/insert text/` - Insert `insert text` before each line matched by `pattern`.
  - `d/pattern/` - Delete lines matching `pattern`.
  - `p/pattern/` - Print lines matching pattern.
  - `n/pattern/` - Get the next line matching pattern.
  - `w//new content/` - Write `new content` to the specified file.
  - `L` - List all available commands.
- **List Available Commands**:

  ```sh
  python SediEdi.py 'L' 
  ```

- **Write New Content**: Write "new content" to `sample.txt`:

  ```sh
  python Sed.py 'w//new content/' sample.txt
  ```

- **Substitute (`s`)**: Replace a pattern with a replacement on lines 1 to 5:

  ```sh
  python Sed.py '1,5s/on/forward/' sample.txt
  ```

- **Append (`a`)**: Append text after each line matched by a pattern on lines 1 to 10:

  ```sh
  python Sed.py '1,10a/sample/append this text/' sample.txt
  ```

- **Insert (`i`)**: Insert text before each line matched by a pattern on all lines:

  ```sh
  python Sed.py 'i/sample/insert this text/' sample.txt
  ```

- **Delete (`d`)**: Delete lines matching a pattern on lines 3 to 7:

  ```sh
  python Sed.py '3,7d/sample/' sample.txt
  ```
  
- **Print ('p')**: Print lines matching "sample":
  ```sh
  python Sed.py 'p/sample/' sample.txt
  ```
 
- **Next Line ('n')**:  Get the next line after the one matching "sample":
  ```sh
  python Sed.py 'n/sample/' sample.txt
  ```
