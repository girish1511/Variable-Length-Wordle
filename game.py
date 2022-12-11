import random
import os
import time
import sys

word = "apple"
letters = {chr(i): 0 for i in range(65,91)}

def display(blank_list, guesses, used_letters=[]):
    blank_str = ' '.join(blank_list)
    print(f"\n{blank_str}  Number of guesses left: {guesses}\n")
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
# guess_list = [*word_guess]

def update(word, word_guess):
    blank_list = []
    gt_list = [*word]
    print(gt_list)
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
                print(f"Please enter a word with excatly {len(word)} letters only !!")
                sys.stdout.write('\x1b[1A')
                sys.stdout.write('\x1b[2K')
                time.sleep(1)
            guesses -= 1
            blank_list = update(word, word_guess)
            if blank_list.count('*') == len(word):
                fl = 1
                break
    return fl

while(True):
    print("Welcome to Variable Length Wordle!\n\n")
    fl = play(word)
    if fl:
        print("\nCongratulations you won!!!!")
    else:
        print("\nBetter luck next time!!")
        print(f"The answer is {word}")
    if not yes("Would you like to play again!"):
        break

print("Thank you for playing the game!!")