import os
import requests
import json
import time

DIR = os.path.dirname(__file__)
TREE_PATH = os.path.join(DIR,'word_tree.json')
    
def create_tree(data, word_length=7):
    tree = {}
    for word in data:
        if len(word) not in tree.keys():
            tree[len(word)] = {}
        tree[len(word)] = add_to_tree(word, tree[len(word)])
    return tree
                
def add_to_tree(word, tree):
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
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    resp = requests.get(url).json()[0]
    defs = resp['meanings']
    word_info = {f'Definition {i}': defs[i]['definitions'][0]['definition'] for i in range(len(defs))}
    return word_info

def get_data():
    #https://github.com/dwyl/english-words
    with open('words_alpha.txt','r') as f:
        data = f.read().splitlines()
    
    start = time.time()
    if os.path.exists(TREE_PATH):
        print("Local cache found!")
        print("Loading from cache...")
        with open(TREE_PATH, 'r') as f:
            tree = json.load(f)
    else:
        print("Local cache not found!")
        print("Generating word tree...")
        tree = create_tree(data)
        with open(TREE_PATH, 'w') as f:
            json.dump(tree, f)
    print(f"Time taken for loading data: {time.time()-start}s")
    return data, tree
            
    # word_info = get_word_info('hello')
            
# if __name__=="__main__":
#     main()