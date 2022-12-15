import random
import os
import time
import sys
import utils

word = "apple"
letters = {chr(i): 0 for i in range(65,91)}

def getChar():
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
    c = ''
    while(c not in letters):
        c = getChar()
    return c

def display(blank_list, guesses):
    # blank_str = ' '.join(blank_list)
    # print(f"\n{blank_str}  Number of guesses left: {guesses}\n")
    for i in range(len(blank_list)):
        print(f"\r{' '.join(guesses[i])}")
        print(f"\r{' '.join(blank_list[i])}\n")
    return

# blank_list = [['_']*6]*6
# guesses = [['q']*6]*6#['']*6
# display(blank_list, guesses)
# print(''.join([]))

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
# guess_list = [*word_guess]
def check_win(res):
    if res.count('*') == len(res):
        return True
    else:
        return False
    
def update(word, word_guess):
    blank_list = []
    gt_list = [*word]
    # print(gt_list)
    for i in range(len(word)):
        if word_guess[i] == word[i]:
            blank_list.append('*')
            gt_list.remove(word_guess[i])
        elif word_guess[i] in gt_list:
            blank_list.append('#')
            gt_list.remove(word_guess[i])
        else:
            blank_list.append('_')
    return blank_list

def play_new(word, tree):
    l = len(word)
    blank_list = [['_']*l]*l
    guesses = [[]*l]*l
    num_guess = l
    display(blank_list, guesses)
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
                # else:
                #     print('\n')
            guesses[l - num_guess] = guess
            res = update(word, guess)
            blank_list[l - num_guess] = res
            # blank_list = [blank_list[0]]*5
            sys.stdout.write(f'\x1b[{(3*l+2)}A')
            # sys.stdout.write(f'\x1b[{(3*l+4)}K')
            sys.stdout.flush()
            display(blank_list, guesses)
            if check_win(res):
                fl=1
                sys.stdout.write('\x1b[3k')
            else:
                num_guess -= 1
        else:
            if check_win(res):
                fl=1
        if fl:
            break
    return

# play_new('apple', {'a':1,'b':2})
def play(word, ):
    blank_list = ['_']*len(word)
    guesses = len(word)
    fl = 1            
    while(True):
        if guesses<=0:
            fl = 0
            break
        else:
            display(blank_list, guesses)
            while(True):
                word_guess = input(f"Enter your guess of a {len(word)} letter word: ")
                if len(word_guess) == len(word):
                    break
                print(f"Please enter a word with exactly {len(word)} letters only !!")
                sys.stdout.write('\x1b[2A')
                # sys.stdout.write('\x1b[2K')
            guesses -= 1
            blank_list = update(word, word_guess)
            if blank_list.count('*') == len(word):
                fl = 1
                break
    return fl

# while(True):
#     print("Welcome to Variable Length Wordle!\n\n")
#     fl = play(word)
#     if fl:
#         print("\nCongratulations you won!!!!")
#     else:
#         print("\nBetter luck next time!!")
#         print(f"The answer is {word}")
#     if not yes("Would you like to play again!"):
#         break
# print("Thank you for playing the game!!")

# print("Available letters: a b d c")
# value = input("Enter guess: ")
# sys.stdout.write('\x1b[2A')
# sys.stdout.write('\x1b[2K')
# def getch(letters):
#     for l in letters:
#         if keyboard.is_pressed(l):
#             return l
# print("Enter guess:")
# du = []
    
# while(True):
#     k = getch(['a','b','c'])
#     if k:
#         print(k)
#         print('yes')
#         sys.stdout.flush()
#         break

    
# for _ in range(6):
#     a = ''
#     while(a not in ['a','b']):
#         a = getChar()
#     print(a)

if __name__=="__main__":
    data, word_tree = utils.get_data()
    word = 'apple'
    game_tree = word_tree[str(len(word))].copy()
    play_new(word, game_tree)