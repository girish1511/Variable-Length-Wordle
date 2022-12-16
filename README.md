# Variable-Length-Wordle

A python implementation of the famous New York Times Wordle game for vairable word lengths.

## Description:
### Files and initialization
- Load `utils.py` and `game.py` in the same folder.
- Run the `game.py` in the command line using the command `python3 game.py`
- During the first run(if the tree files are not read) then trees are created and stored in cache files `word_tree.json` and `word_len.json`.

### How to play
- As the program starts, a welcome information is printed. The user is then asked whether he/she wants to select the number of letters of the word. If the user does not want to enter then the program randomly assign the number of letters.
- The layout for the game is created based on the number of letters. Number of letters=Number of guesses
- The user's input is taken character-by-character and for each character read, the possible set of next letters is updated live in the terminal.
- For each guess, for each letter the program matches with the ground-truth word letters. If it matches and is present in the right location then the letter is given green color and if it matches but is present in the wrong location the letter is given yellow. The layout is updated using the color coded guess word.
- Once the game ends in win or lose, the program shows the ground-truth word along with its definition/s.
- The user can decide to play the again or not. If the user decides to play then the screen is cleared and a new game starts.

## Requirements
Only `requests` module is required for the program.

## Data Structure
- `word_tree` is a tree structure made up of letters of the words as nodes. The tree is further segregated by lengths of the words. This gives easy accesbility for the program while getting possible letters in the game.
- `len_tree` is a dictionary with keys as word length and values are list of words with corresponding word length as key.
