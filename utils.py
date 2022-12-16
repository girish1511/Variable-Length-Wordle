import os
import requests
import json
import time

DIR = os.path.dirname(__file__)
TREE_PATH = os.path.join(DIR,'word_tree.json')
WORD_LEN_PATH = os.path.join(DIR,'word_len.json')
    
def create_tree(data):
    """
    Function that generates the word tree based on letters of the word as nodes
    given a list of words

    Parameters
    ----------
    data : list
        List of words in English language

    Returns
    -------
    dict
        A tree with letters of the words as nodes and structured in nested dictionary format
    """
    tree = {}
    for word in data:
        if word.isalpha() and word.islower():
            if str(len(word)) not in tree.keys():
                tree[str(len(word))] = {}
            tree[str(len(word))] = add_to_tree(word, tree[str(len(word))])
    return tree

def create_len_data(data):
    """
    Function that creates a dictionary using words list with keys as the length of the word
    and values as the list of words of length stated by the key

    Parameters
    ----------
    data : list
        List of words in English language

    Returns
    -------
    dict
        Dictionary with key: value pair as k: [word if len(word)==k]
    """
    len_data = {}
    for word in data:
        if word.isalpha() and word.islower():
            if str(len(word)) not in len_data.keys():
                len_data[str(len(word))] = []
            len_data[str(len(word))].append(word)
    return len_data
               
def add_to_tree(word, tree):
    """
    Recursively create nodes and update the tree with the letters of <word>

    Parameters
    ----------
    word : str
        Word to be added to the tree
    tree : dict
        Tree that needs to be updated

    Returns
    -------
    dict
        Updated tree that contains the word
    """
    if len(word)==1:
        try:
            tree[word] = '.'
            return tree
        except:
            return {word: '.'}
    else:
        tree[word[0]] = add_to_tree(word[1:], tree[word[0]] if word[0] in tree.keys() else dict())
        return tree
   
def get_word_info(word):
    """
    Call the FreeDictionaryAPI to get the definition of the word

    Parameters
    ----------
    word : str
        Word whose definition is required

    Returns
    -------
    dict or None
        Dictionary of definitions if the API found the word's meaning else returns None
    """
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    try:
        resp = requests.get(url).json()[0]
        defs = resp['meanings']
        word_info = {f'Definition {i}': defs[i]['definitions'][0]['definition'] for i in range(len(defs))}
    except:
        word_info = None
    return word_info

def get_data():
    """
    Function checks whether the cache files for word tree and word length tree are present
    If the cache is not present then the tree is created else the data is loaded from cache

    Returns
    -------
    dict, dict
        Returns word length tree containings list of words segregated based on the length of the word
        and word tree created with nodes as letters of the word
    """
    #https://github.com/dwyl/english-words
    with open('words_alpha.txt','r') as f:
        data = f.read().splitlines()
    
    start = time.time()
    if os.path.exists(TREE_PATH):
        print("Local cache for tree found!")
        print("Loading from cache...")
        with open(TREE_PATH, 'r') as f:
            tree = json.load(f)
    else:
        print("Local cache for tree not found!")
        print("Generating word tree...")
        tree = create_tree(data)
        with open(TREE_PATH, 'w') as f:
            json.dump(tree, f)
    print(f"Time taken for loading tree data: {time.time()-start}s") 
           
    start = time.time()       
    if os.path.exists(WORD_LEN_PATH):
        print("Local cache for tree found!")
        print("Loading from cache...")
        with open(WORD_LEN_PATH, 'r') as f:
            len_data = json.load(f)
    else:
        print("Local cache for tree not found!")
        print("Generating word length tree...")
        len_data = create_len_data(data)
        with open(WORD_LEN_PATH, 'w') as f:
            json.dump(len_data, f)
    print(f"Time taken for loading word data: {time.time()-start}s", end="\n\n\n")
    return len_data, tree
            
    # word_info = get_word_info('hello')
            
# if __name__=="__main__":
#     get_data()