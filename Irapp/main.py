# main.py
import glob
import math
import os
import re
import sys
from collections import defaultdict
from functools import reduce

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

# Download NLTK resources if not already downloaded
nltk.download('punkt')
nltk.download('stopwords')

# Constants
STOPWORDS = set(stopwords.words("english"))
CORPUS = "documents/*"

# Global variables
document_filenames = dict()  # Mapping of document ids to filenames
N = 0  # Number of documents in the corpus
vocabulary = set()  # Set of all unique terms (words) in the corpus
postings = defaultdict(dict)  # Dictionary where keys are terms and values are postings lists
document_frequency = defaultdict(int)  # Dictionary to store document frequencies of terms
length = defaultdict(float)  # Dictionary to store document vector lengths

# Initialize Porter Stemmer for stemming
stemmer = PorterStemmer()

def preprocess_text(text):
    tokens = nltk.word_tokenize(text.lower())  # Tokenization and lowercasing
    tokens = [word for word in tokens if word.isalnum()]  # Remove punctuation
    tokens = [stemmer.stem(word) for word in tokens if word not in STOPWORDS]  # Remove stopwords and stem
    return tokens

def initialize_ir_system():
    global N
    get_corpus()
    initialize_terms_and_postings()
    initialize_document_frequencies()
    initialize_lengths()
    print("Initialization complete.")
    print(f"Number of documents: {N}")
    print(f"Vocabulary size: {len(vocabulary)}")
    print(f"Document frequencies: {document_frequency}")
    print(f"Document lengths: {length}")

def get_corpus():
    global document_filenames, N
    documents = glob.glob(CORPUS)
    N = len(documents)
    document_filenames = dict(zip(range(N), documents))
    print(f"Documents found: {documents}")

def initialize_terms_and_postings():
    global vocabulary, postings
    for id in document_filenames:
        with open(document_filenames[id], "r", encoding="utf-8") as f:
            document = f.read()

        terms = preprocess_text(document)
        unique_terms = set(terms)
        vocabulary = vocabulary.union(unique_terms)

        for term in unique_terms:
            postings[term][id] = terms.count(term)
    print(f"Vocabulary: {vocabulary}")
    print(f"Postings: {postings}")

def initialize_document_frequencies():
    global document_frequency
    for term in vocabulary:
        document_frequency[term] = len(postings[term])

def initialize_lengths():
    global length
    for id in document_filenames:
        l = 0
        for term in vocabulary:
            l += term_frequency(term, id) ** 2
        length[id] = math.sqrt(l)

def term_frequency(term, id):
    if id in postings[term]:
        return postings[term][id]
    else:
        return 0.0

def inverse_document_frequency(term):
    if term in vocabulary:
        return math.log(N / document_frequency[term], 2)
    else:
        return 0.0

def do_search(query):
    query_tokens = preprocess_text(query)
    print(f"Processed query tokens: {query_tokens}")
    scores = [(id, similarity(query_tokens, id)) for id in range(N)]
    print(f"Similarity scores: {scores}")
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    results = [(document_filenames[id], score) for id, score in sorted_scores if score > 0]  # Filter out zero scores
    print(f"Search results: {results}")
    return results

def similarity(query, id):
    similarity = 0.0
    for term in query:
        if term in vocabulary:
            similarity += term_frequency(term, id) * inverse_document_frequency(term)
    if length[id] > 0:
        similarity /= length[id]
    return similarity

