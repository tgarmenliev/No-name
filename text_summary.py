import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import scipy as sp


def read_article(file_name):
    file = open(file_name, "r")
    filedata = file.readlines()
    article = filedata[0].split(". ")
    sentences = []
    for sentecnes in article:
        sentences.append(sentecnes.replace("[^a-zA-Z]", " ").split(". "))
    sentences.pop()
    return sentences

def sentence_similarity(sent1, sent2, stopwords = None):
    if stopwords is None:
        stopwords = []
    
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1 + sent2))
    
    vector1 = [0] *len(all_words)
    vector2 = [0] *len(all_words)
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
    
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    
    return 1 - cosine_distance(vector1, vector2)

def gen_sim_matrix(sentences, stop_words):
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
    for inx1 in range(len(sentences)):
        for inx2 in range(len(sentences)):
            if inx1 == inx2:
                continue
            similarity_matrix[inx1][inx2] = sentence_similarity(sentences[inx1], sentences[inx2], stop_words)
    return similarity_matrix

def sentences_nb(file_name):
    

    num_lines = 0

    with open(file_name, 'r') as f:
        for line in f:
            words = line.split()

            num_lines += 1
           
    
    return num_lines


def generate_summary(file_name, top_n = 5):
    stop_words = stopwords.words('english')
    summerize_text = []
    num_lines = sentences_nb(file_name)
    if num_lines <= 2:
        file_ptr = open(file_name, "r")
        string = file_ptr.read()
        print("Summary:", string)
        return string

    sentences = read_article(file_name)
    sentence_similarity_matrix = gen_sim_matrix(sentences, stop_words)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentence = sorted(((scores[i], s)for i,s in enumerate(sentences)),reverse=True)
    for i in range(top_n):
        summerize_text.append(" ".join(ranked_sentence[i][1]))
    
    print("Summary: \n", ". ".join(summerize_text))
    




generate_summary("C:\\Users\\User\\Documents\\file.c\\ddz.txt", 2)
