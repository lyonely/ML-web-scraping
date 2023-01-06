from typing import List, Dict
# import re
from rake_nltk import Rake
import requests
import numpy as np
from re import sub
from gensim.utils import simple_preprocess
import gensim.downloader as api
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import WordEmbeddingSimilarityIndex
from gensim.similarities import SparseTermSimilarityMatrix
from gensim.similarities import SoftCosineSimilarity


class NLPModel:
    """ NLPModel object that uses a question_answerer model """

    def __init__(self):
        """ Initializes a NLPModel object with a model input"""
        self.rake = Rake()
        self.max_searches = 32
        self.model_link = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

    def get_keywords(self, question: str, num: int):
        """ Extracts relevant keywords from question """
        self.rake.extract_keywords_from_text(question)
        try:
            return str(self.rake.get_ranked_phrases()[0]).split(" ")[:num]
        except IndexError:
            return []

    def use_model(self, question, context):
        """ Uses huggingface inference api to pass through question and context to roberta model"""
        result_response = requests.post(self.model_link,
        headers={"Authorization": "Bearer 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"},
        json={
            "inputs": {
                "question": question,
                "context": context
            },
        },
        timeout=5)

        return result_response.json()

    # pylint: disable-next=too-many-locals, too-many-branches
    def product_question(self, tags: List[str], question: str):
        """ get all tags of soup """
        results: Dict[str, int] = {}
        # max_answer represents the answer with the highest confidence
        keywords = set(self.get_keywords(question, num=3))
        search = 1
        tags_visited = {}
        tags = [tag for tag in tags if len(tag) < 700]
        for tag in tags:
            if search > self.max_searches:
                break

            contain = len(keywords) == 0
            weight = 0 + int(contain)
            for word in keywords:
                if word in tag:
                    contain = True
                    weight += 0.5

            if contain:
                ignore_flag = True
                for visited, item in tags_visited:
                    if visited in tag and item >= 2:
                        ignore_flag = False
                        break

                if ignore_flag:
                    if tag in tags_visited:
                        tags_visited[tag] += 1
                    else:
                        tags_visited[tag] = 1

                    result = self.use_model(question, tag)

                    if result["answer"] in results:
                        results[result["answer"]] += result["score"] / search * weight
                    else:
                        results[result["answer"]] = result["score"] / search * weight

                    search += 1
        answer = ""
        if results:
            answer = max(results, key=results.get)

        if ">" in answer:
            if message := re.findall(r">(.*)<?", answer):
                answer = message[0]
        if "<" in answer:
            if message := re.findall(r"(.*)<", answer):
                answer = message[0]

        return answer

    def alternate_algorithm(self, soup, question):
        """ Alternative algorithm """
        found = re.findall(r">([^<]*\S)<", soup)
        found = [f for f in found if len(f) < 500]
        results = {}
        for tag in found:

            result = self.use_model(question, tag)

            if result["answer"] in results:
                results[result["answer"]] += result["score"]
            else:
                results[result["answer"]] = result["score"]
        print(results)
        answer = ""
        if results:
            answer = max(results, key=results.get)
        print(answer)

    def distanceCheck():

        websites = []
        questions = []
        answers = []


        """
        News sites:

        """

        searches_params = [2, 4, 8, 16, 32, 64]
        tags_params = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        visits_params = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        total_Lev_dist = 0
        for search in searches_params:
            for tag in tags_params:
                for visits in visits_params:
                    for i in range(len(websites)):
                        ws = websites[i]
                        q = questions[i]
                        a = answers[i]
                        
                        # Perform the qna with the model and populate result with it
                        result = ""

                        total_Lev_dist += levDist(result, a)
                        
        return total_Lev_dist / len(websites)

    
    def levDist(pred, gold):
        dists = numpy.zeros((len(pred) + 1, len(gold) + 1))

        for i in range(len(pred) + 1):
            dists[i][0] = i
        
        for j in range(len(gold) + 1):
            dists[0][j] = j

        x = 0
        y = 0
        z = 0

        for i in range(1, len(pred) + 1):
            for j in range(1, len(gold) + 1):
                if (pred[i - 1] == gold[j - 1]):
                    dists[i][j] = dists[i - 1][j - 1]
                else:
                    x = dists[i][j - 1]
                    y = dists[i - 1][j]
                    z = dists[i - 1][j - 1]

                    if (x <= y and x <= z):
                        dists[i][j] = x + 1
                    if (y <= x and y <= z):
                        dists[i][j] = y + 1
                    else:
                        dists[i][j] = z + 1
    
        return dists[len(pred)][len(gold)]

    stopwords = ['the', 'and', 'are', 'a']

    def preprocess(str):
        str = sub(r'<img[^<>]+(>|$)', " image_token ", str)
        str = sub(r'<[^<>]+(>|$)', " ", str)
        str = sub(r'\[img_assist[^]]*?\]', " ", str)
        str = sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " url_token ", str)
        return [token for token in simple_preprocess(str, min_len=0, max_len=float("inf")) if token not in stopwords]


    def similarityCheck(pred, gold):
        procPred = preprocess(pred)
        procGold = preprocess(gold)

        glove = api.load("glove-wiki-gigaword-50")    
        similarity_index = WordEmbeddingSimilarityIndex(glove)

        dictionary = Dictionary(procGold+[procPred])
        termFreq = TfidfModel(dictionary=dictionary)

        similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary, termFreq)

        query_tf = termFreq[dictionary.doc2bow(procPred)]

        index = SoftCosineSimilarity(
            termFreq(dictionary.doc2bow(procGold),
            similarity_matrix))

        similarity_score = index[query_tf]

        return similarity_score
