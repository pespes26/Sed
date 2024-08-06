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

-*If the pattern is found, it prints the relevant lines.
-*If the pattern is not found, it prints a proper message.
-*After all commands are executed, it prints the final content.

### Help
To display the help message with the available commands:
```bash
python BasicSed.py -f "L"
```

### Exit Values

- `0`: Successful completion.
- `>0`: An error occurred.

#### Example File Content

The quick brown fox jumps over the lazy dog.
Python is a versatile programming language.
Regular expressions can be tricky to master.
Text manipulation is a common task in scripting.
Efficient code can save a lot of time.
Debugging is an essential skill for developers.
Learning new tools can improve productivity.
This sentence contains the word pattern.
Automation is key to handling repetitive tasks.
Version control systems like Git are important.
Data processing requires attention to detail.
Understanding algorithms is fundamental to programming.
The sun rises in the east and sets in the west.
A journey of a thousand miles begins with a single step.
Practice makes perfect.
All that glitters is not gold.
A picture is worth a thousand words.
Actions speak louder than words.
An apple a day keeps the doctor away.
Brevity is the soul of wit.
A stitch in time saves nine.
Birds of a feather flock together.
Better late than never.
Curiosity killed the cat.
Don't count your chickens before they hatch.
Every cloud has a silver lining.
Fortune favors the brave.
Honesty is the best policy.
If it ain't broke, don't fix it.
It's no use crying over spilled milk.
Knowledge is power.
Laughter is the best medicine.
Money can't buy happiness.
Necessity is the mother of invention.
No man is an island.
Old habits die hard.
Opportunity knocks but once.
Patience is a virtue.
Practice what you preach.
Rome wasn't built in a day.
The early bird catches the worm.
The pen is mightier than the sword.
The squeaky wheel gets the grease.
There's no place like home.
Time flies when you're having fun.
To err is human, to forgive divine.
Two heads are better than one.
When in Rome, do as the Romans do.



