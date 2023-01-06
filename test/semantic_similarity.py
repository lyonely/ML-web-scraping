from re import sub
import numpy as np
from gensim.utils import simple_preprocess
import gensim.downloader as api
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import WordEmbeddingSimilarityIndex
from gensim.similarities import SparseTermSimilarityMatrix
from gensim.similarities import SoftCosineSimilarity

stopwords = ['the', 'and', 'are', 'a']
def preprocess(str):
    str = sub(r'<img[^<>]+(>|$)', " image_token ", str)
    str = sub(r'<[^<>]+(>|$)', " ", str)
    str = sub(r'[imgassist[^]]*?]', " ", str)
    str = sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " url_token ", str)
    return [token for token in simple_preprocess(str, min_len=0, max_len=float("inf")) if token not in stopwords]


def similarityCheck(pred, gold):
    procPred = preprocess(pred)
    procGold = preprocess(gold)
    print(procPred)
    print(procGold)

    glove = api.load("glove-wiki-gigaword-50")
    similarity_index = WordEmbeddingSimilarityIndex(glove)

    dictionary = Dictionary([procGold]+[procPred])
    tfidf = TfidfModel(dictionary=dictionary)

    similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary, tfidf)

    query_tf = tfidf[dictionary.doc2bow(procPred)]

    index = SoftCosineSimilarity(
        tfidf[dictionary.doc2bow(procGold)],
        similarity_matrix)

    similarity_score = index[query_tf]

    return similarity_score

# DOES NOT WORK WITH NUMBERS AS ONLY WORDS ARE ENCODED
print(similarityCheck("a cat is a dog", "water under the bridge"))