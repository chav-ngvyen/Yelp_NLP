import json
import re
from tqdm import tqdm

from textblob import Word
from typing import List
import pandas as pd
import numpy as np

import multiprocessing; cores = multiprocessing.cpu_count() # Count the number of cores in a computer

# Get business category:
def get_cat(biz_cat, yelp_cat):
    i = 0
    while (i < len(biz_cat)):    
        for cat in biz_cat:
            if cat in yelp_cat:
                return cat, yelp_cat.index(cat)
        break
    else:
        return (-1, "not in list")

# Split at capitalize words and add underscore
def convert_category(cat: List):
    arr = []
    for i in cat:
        i = i.lower()
        i = re.sub(r"'s","", i)#remove 's  
        # i = Word(i).singularize() #singularize plurals
        i = re.sub(r"[^a-zA-Z0-9]"," ", i) #remove all other special characters and lowercase
        i = Word(i).singularize() #singularize plurals
        i = "_".join(i.split()) #join tokens with underscore
        arr.append(i)       
    return arr

# Decontract text
def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", str(phrase))
    phrase = re.sub(r"can\'t", "can not", str(phrase))

    # general
    phrase = re.sub(r"n\'t", " not", str(phrase))
    phrase = re.sub(r"\'re", " are", str(phrase))
    phrase = re.sub(r"\'s", " is", str(phrase))
    phrase = re.sub(r"\'d", " would", str(phrase))
    phrase = re.sub(r"\'ll", " will", str(phrase))
    phrase = re.sub(r"\'t", " not", str(phrase))
    phrase = re.sub(r"\'ve", " have", str(phrase))
    phrase = re.sub(r"\'m", " am", str(phrase))
    return phrase

# Preprocess text
def preprocess(text_column):
    my_list = []
    # tqdm is for printing the status bar
    for sentance in tqdm(text_column.values):
        sent = decontracted(sentance)
        sent = sent.replace('\\r', ' ')
        sent = sent.replace('\\"', ' ')
        sent = sent.replace('\\n', ' ')
        sent = sent.replace('www', '')
        sent = sent.replace('https', '')
        sent = sent.replace('http', '')
        sent = re.sub('[^A-Za-z0-9]+', ' ', sent)
        # https://gist.github.com/sebleier/554280
        sent = ' '.join(e.lower() for e in sent.split())
        my_list.append(sent.lower().strip())
    
    return my_list