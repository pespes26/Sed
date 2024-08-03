# SediEdi.py

A limited version of the sed utility implemented in Python, supporting basic text editing commands with addresses.

## Features

- **Addresses**: Supports line number addresses and context addresses using Basic Regular Expressions (BREs).
- **Commands**: Supports the following commands:
  - s: Substitute a pattern with a replacement.
  - a: Append text after each line matched by a pattern.
  - i: Insert text before each line matched by a pattern.
  - d: Delete lines matching a pattern.
  - w: Write new content to a file.
  - l: List all available commands.

## Usage

### Command Format

The command format is:

[address[,address]]command/pattern/replacement_or_text/


### Examples

- **List Available Commands**:

  
sh
  python SediEdi.py 'l///'


- **Write New Content**: Write "new content" to sample.txt:

  
sh
  python SediEdi.py 'w//new content/' sample.txt


- **Substitute (s)**: Replace a pattern with a replacement on lines 1 to 5:

  
sh
  python SediEdi.py '1,5s/on/forward/' sample.txt


- **Append (a)**: Append text after each line matched by a pattern on lines 1 to 10:

  
sh
  python SediEdi.py '1,10a/sample/append this text/' sample.txt


- **Insert (i)**: Insert text before each line matched by a pattern on all lines:

  
sh
  python SediEdi.py 'i/sample/insert this text/' sample.txt


- **Delete (d)**: Delete lines matching a pattern on lines 3 to 7:

  
sh
  python SediEdi.py '3,7d/sample/' sample.txt


- **Reading from Standard Input**:
  
sh
  echo "example text" | python SediEdi.py 's/text/STRING//'


## Details

- **Addresses**:

  - A single decimal number to specify a line number.
  - A $ character to specify the last line.
  - A context address with a Basic Regular Expression (BRE) enclosed in delimiters, usually slashes (/).
  - Omitting an address selects every line.

- **Editing Commands**:
  - s/pattern/replacement/ - Substitute pattern with replacement.
  - a/pattern/append text/ - Append append text after each line matched by pattern.
  - i/pattern/insert text/ - Insert insert text before each line matched by pattern.
  - d/pattern/ - Delete lines matching pattern.
  - w//new content/ - Write new content to the specified file.
  - l/// - List all available commands.