import random
import os
import time
import sys
import utils

#This function is the only one, among the entire code, taken from the internet and not my own.
#https://stackoverflow.com/a/36974338
def getChar():
    """
    Accepts only a single character from the terminal as an input, and the character is read without 
    the need to press enter.

    Returns
    -------
    char
        A single character read as input
    """
    try:
        # for Windows-based systems
        import msvcrt # If successful, we are on Windows
        return msvcrt.getch()

    except ImportError:
        # for POSIX-based systems (with termios & tty support)
        import tty, sys, termios  # raises ImportError if unsupported

        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)
            answer = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)

        return answer

def get_specific_letters(letters):
    """
    Function that accepts a single character provided it is present in <letters>.
    The function keeps running until the user enters a character present in <letters>

    Parameters
    ----------
    letters : list
        Allowed list of characters as input

    Returns
    -------
    char
        Single character entered by the user and present in <letters>
    """
    c = ''
    while(c not in letters):
        c = getChar()
    return c

def display(blank_list):
    """
    Function that is in-charge of printing the layout in the desired format based
    on the strings and characters present in <blank_list>

    Parameters
    ----------
    blank_list : list(list)
        List of lists consisting of information on characters and their color to be
        printed in the layout
    """
    # sys.stdout.write("\x1b[K\n"*(2*len(blank_list)+2))
    # sys.stdout.flush()
    for i in range(len(blank_list)):
        print(f"\r{'  '.join(blank_list[i])}\n")
    return

def yes(prompt):
    """
    Function that's returns a boolean based on the response given for a prompt

    Parameters
    ----------
    prompt : str
        A prompt to request a response from the user

    Returns
    -------
    bool
        True if the response is a variation of yes else False if the reponse is a variation of no
    """
    while(True):
        ans = input(prompt.lower().capitalize()).lower()
        if ans in ['yes', 'y', 'yup', 'sure']:
            return True
        elif ans in ['no', 'n', 'nope']:
            return False
        else:
            print('Please enter a valid response!!')
    
def update(word, word_guess):
    """
    Function that color codes the letters based on the rules of the Wordle game.
    Letters of <word_guess> that match and are present in the right location are
    assigned green and letters that match but are in the wrong location are assigned
    yellow. Two for loops are used to take care of words containing non-unique set of
    letters. `\\033[32m` assigns green color to text in terminal and
    `\\033[33m` assigns yellow color to text in terminal. `\\033[0m]` is to let the
    terminal know the endpoint

    Parameters
    ----------
    word : str
        The ground-truth word that needs to be guessed
    word_guess : list(char)
        The user's guess as list of char for the ease of manipulation and updation

    Returns
    -------
    list(list), int
        Updated <blank_list> that contains information on the correctness of the
        user's guess. Second argument returns the count of all the letters that
        matched and where in the correct location
    """
    blank_list = ['']*len(word)
    gt_list = [*word]
    # count = 0
    mark = [0]*len(word)
    
    for i in range(len(word)):
        if word_guess[i] == word[i]:
            blank_list[i] = f'\033[32m{word_guess[i].upper()}\033[0m'
            gt_list.remove(word_guess[i])
            mark[i] = 1
            
    for i in range(len(word)):
        if not mark[i]:
            if word_guess[i] in gt_list:
                blank_list[i] = f'\033[33m{word_guess[i].upper()}\033[0m'
                gt_list.remove(word_guess[i])
            else:
                blank_list[i] = word_guess[i].upper()

    return blank_list, sum(mark)

def play_new(word, tree):
    """
    Functions that also the user to interact with the program and play the game.
    The number of guesses is set to be equal to the length of the word to ensure
    a fair and fun game. <blank_list> is initialized with underscores for all the
    letters and all the guesses. <blank_list> is updated throughout the game comparing
    the user's input with the ground-truth value.

    Parameters
    ----------
    word : str
        Ground-truth value
    tree : dict
        Dictionary made up of letters of the words as nodes.

    Returns
    -------
    bool
        Boolean that gives teh conclusion of the game i.e., win or lose
    """
    l = len(word)
    blank_list = [['_']*l]*l
    num_guess = l
    display(blank_list)#, guesses)
    
    fl=0
    while(True):
        if num_guess>0:
            temp_tree = tree.copy()
            guess = []
            for _ in range(l):
                avail_letters = list(temp_tree.keys())
                print(f"\rPossible letters: {' '.join(avail_letters)}")
                print(f"\rEnter your guess:")
                sys.stdout.write('\x1b[K')
                print(f"\r{''.join(guess)}", end="", flush=True)
                c = get_specific_letters(avail_letters)
                temp_tree=temp_tree[c]
                guess.append(c)
                if len(guess)<l:
                    sys.stdout.write('\x1b[2A')
                    sys.stdout.write('\x1b[2K')
            res, count = update(word, guess)
            blank_list[l - num_guess] = res
            sys.stdout.write(f'\x1b[{(2*l+2)}A')
            # sys.stdout.write('\x1b[K')
            display(blank_list)#, guesses)
            if count==l:
                fl=1
                break
            else:
                num_guess -= 1
        else:
            if count==l:
                fl=1
            break
    return fl

def intro_display():
    """
    Function that displays the intro for the game that includes instructions and disclaimers
    """
    ins = ["The possible letters displayed are to guide to enter only valid English words",
           "\033[;32mGreen\033[0m color indicates that the letter is present in the word and at the right location",
           "\033[;33mYellow\033[0m color indicates that the letter is present in the word but at the wrong location"]
    disclaim = "Disclaimer: Although most of the offsensive words have been removed, some might remain! Play with caution!"
    print("\033[4;1mWelcome to Variable Length Wordle!\033[0m".center(100), end="\n\n")
    print("The objective of the game is to guess the word within the given number of tries!!\n".center(100))
    print("Instructions:")
    for i in ins:
        print(f"- {i}")
    print(f"\033[7;1m{disclaim}\033[0m", end='\n\n')
    return

def get_random_word(len_data):
    """
    Function asks the user if they want to decide the length of the word to be played. If the user
    doesn't then the program randomly selects one. The length of the word is kept between 4 and 6
    (both inclusive) to ensure a fun, stress-free game. Another reason for the upper limit is that
    for some reason the limit to the number of lines allowed to move up the terminal via escape 
    sequence is 20(not entirely sure). This might be a local error, nevertheless, to avoid issues the upper limit is
    set to 6.
    
    With the <word_len> decided as above, the program selected a word of length <word_len> by using
    the <len_data> tree created at the beginning by calling <utils.get_data()> 

    Parameters
    ----------
    len_data : dict
        Dictionary with key: value pair as k: [word if len(word)==k]

    Returns
    -------
    str
        The ground-truth word that is to be guessed
    """
    word_len = None
    l_lim = 4
    u_lim = 6
    if yes("Would you like to select how many lettered word you want to play the game with: "):
        while(True):
            try:
                word_len = int(input(f"Enter how many lettered word you want to play the game with(between {l_lim} and {u_lim} both inclusive): "))
            except:
                print("Please enter a numeric value!!!")
                
            if l_lim<=word_len<=u_lim:
                break
            print(f'Please enter length between {l_lim} and {u_lim} (both inclusive)!!')
    else:
        print("Randomly selecting the length of the word!!!")
        word_len = random.randint(l_lim,u_lim)
    word = random.choice(len_data[str(word_len)])
    return word

def result_display(fl, word):
    
    """
    Function to display the results of the game. Additionally to make the game more
    informative, the program enters the definition/s of the ground-truth word. If the
    API fails to get a definition, then a google search link is provided for the
    convenience of the user
    """
    
    sys.stdout.write('\x1b[K\n'*3) #Clears the next 3 lines
    
    if fl:
        print("Congratulations you won!!!!".upper().center(100), end="\n\n", flush=True)
    else:
        print("You lost!! Better luck next time!!".upper().center(100), end="\n\n", flush=True)
    print(f"The word is \033[3;1m{word}\033[0m".center(100))
    print("Definitions: ")
    word_info = utils.get_word_info(word)
    if word_info:
        for d in word_info.values():
            print(f"- {d}")
    else:
        print("No definition found on the API!!!")
        print(f"Link to google search for the definition: https://www.google.com/search?q={word}")
    print("\n")
    

if __name__=="__main__":
    #Get the word length tree and word tree by checking
    #if the cache is present
    len_data, word_tree = utils.get_data()
    
    while(True):
        os.system('clear')
        intro_display()
        word = get_random_word(len_data)
        game_tree = word_tree[str(len(word))].copy()
        fl = play_new(word, game_tree)
        result_display(fl, word)
        if not yes("Would you like to play again!: "):
            break
    print(f"\nThank you for playing the game!!\n")
    text = str()