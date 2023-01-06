from typing import List, Dict
from rake_nltk import Rake
import re
import numpy as np
from re import sub
from gensim.utils import simple_preprocess
import gensim.downloader as api
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.similarities import WordEmbeddingSimilarityIndex
from gensim.similarities import SparseTermSimilarityMatrix
from gensim.similarities import SoftCosineSimilarity

from backend.timer import timed

class NLPModel:
    """ NLPModel object that uses a question_answerer model """

    def __init__(self, question_answerer, site_kind):
        """ Initializes a NLPModel object with a model input"""
        self.raker = Rake()
        self.question_answerer = question_answerer

        self.MAX_SEARCHES = 32
        # if site_kind == "news_site":
        #     self.MAX_SEARCHES = 32
        # elif site_kind == "supermarket_site":
        #     self.MAX_SEARCHES = 15


        # self.MAX_SEARCHES = 32 #should depend on kind of site
        self.NUM_KEYWORDS = 10
        self.MAX_TAG_LENGTH = 700
        self.MAX_VISITS_PER_TAG = 2
    


    #n / m => (n + 1) / (m + 2)


    
    def get_keywords(self, question: str, n: int = 1):
        self.raker.extract_keywords_from_text(question)
        return str(self.raker.get_ranked_phrases()[0]).split(" ")[:n]

    
    @timed
    def product_question(self, tags: List[str], question: str):
        """
        IDEAS TO REDUCE THE NUMBER OF TIMES WE CALL THE MODEL

        1. make contain more strict (maybe a certain percentage has to contain the words?)
        2. make tags a shorter list - self.MAX_TAG_LENGTH can be shorter
        3. shouldn't we remove all the html from visited? ie just be left with the text
        4. make numsearches shorter
        5. maybe tune max_searches depending on type of website
        
        """
        """ get all tags of soup """
        results: Dict[str, int] = {}
        # max_answer represents the answer with the highest confidence
        keywords = self.get_keywords(question, self.NUM_KEYWORDS)
        print(keywords)
        tags_visited = {}
        tags = [tag for tag in tags if len(tag) < self.MAX_TAG_LENGTH]
        print("Starting the algorithm")
        model_call_count = 0
        num_searches = 1

        # sorted_tags = sorted(tags, key = len)
        sorted_tags = tags

        #idea: join tags together so that we call the model less times
        max_tag_length = 100
        loop_tags = []
        curr = ""
        i = 0
        while i < len(sorted_tags):
            while(len(curr) < max_tag_length and i < len(sorted_tags)):
                curr = curr + sorted_tags[i]
                i += 1
            loop_tags.append(curr)
            curr = ""

        print("loop tags length", len(loop_tags))
        print("tags length", len(tags))
        for tag in sorted_tags:
            if num_searches > self.MAX_SEARCHES:
                break
            word_map = [word in tag for word in keywords]
            contain = any(word_map)
            weight = sum(word_map) * 0.5

            if contain:
                    ignore_flag = False
                        

                    for visited in tags_visited.keys():
                        text_tag = re.sub("\<.*?\>", "", tag)
                        if (visited in text_tag or text_tag in visited) and tags_visited[visited] >= self.MAX_VISITS_PER_TAG:
                            ignore_flag = True 
                            break

                    if not ignore_flag:
                        if tag in tags_visited:
                            tags_visited[tag] += 1
                        else:
                            tags_visited[tag] = 1


                        #print("calling model")
                        model_call_count += 1
                        print("Calling model on question: " + str(question) + ", context: ", str(tag))
                        result = self.question_answerer(question=question, context=tag)
                        score_to_add = result["score"] / num_searches * weight

                        if result["answer"] in results:
                            results[result["answer"]] += score_to_add
                        else:
                            results[result["answer"]] = score_to_add

        




        print("num times called model", model_call_count)
        print(results)
        answer = ""
        if results:
            answer = max(results, key=results.get)

        if ">" in answer:
            if m := re.findall(r">(.*)<?", answer):
                answer = m[0]
        if "<" in answer:
            if m := re.findall(r"(.*)<", answer):
                answer = m[0]

        print("Here's the answer:", answer)
        return answer

    def distanceCheck():
        """
        Shopping sites:
        W: https://www.tesco.com/clubcard/clubcard-plus/?sc_cmp=ref*tdchp*stc*tesco.com*new_homepage_taxonomy&utm_source=tesco.com_homepage&utm_medium=tesco.com&utm_campaign=new_homepage_taxonomy
        Q: How much do I pay per month?
        A: £7.99

        W: https://www.teso.com/groceries/en-GB/products/311267977
        Q: How many calories does this contain?
        A: 6 cal

        W: https://www.tesco.com/groceries/en-GB/products/255985687
        Q: How many slices does this contain?
        A: 12 slices

        W: https://www.tesco.com/groceries/en-GB/products/299772342
        Q: Where to use this?
        A: Toilet

        W: https://www.tesco.com/groceries/en-GB/products/313606076
        Q: How to recycle?
        A: Box. Recycle Film. Don't Recycle Tray. Recycle

        W: https://www.tesco.com/groceries/en-GB/products/311261278
        Q: How far should you hold it?
        A: 72H

        W: https://www.tesco.com/groceries/en-GB/products/303206081
        Q: What are dimensions?
        A: H16cm x W27cm x D29cm

        W: https://www.zara.com/uk/en/vertical-textured-sweatshirt-p06462401.html?v1=229687668&v2=2113165
        Q: what is the maximum ironing temperature?
        A: 110C/230F

        W: 
        Q:
        A:

        
        """

        websites = ["https://www.tesco.com/clubcard/clubcard-plus/?sc_cmp=ref*tdchp*stc*tesco.com*new_homepage_taxonomy&utm_source=tesco.com_homepage&utm_medium=tesco.com&utm_campaign=new_homepage_taxonomy",
                    ]
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



    def product_question_prime(self, tags: List[str], question: str):
        
        """ get all tags of soup """
        results: Dict[str, int] = {}
        # max_answer represents the answer with the highest confidence
        keywords = self.get_keywords(question, self.NUM_KEYWORDS)
        print(keywords)
        tags_visited = {}
        tags = [tag for tag in tags if len(tag) < self.MAX_TAG_LENGTH]
        print("Starting the algorithm")
        model_call_count = 0
        for tag in tags:
            word_map = [word in tag for word in keywords]
            contain = any(word_map)
            weight = sum(word_map)

            if contain:
                for num_searches in range(1, self.MAX_SEARCHES +1):
                        ignore_flag = False
                        

                        for visited in tags_visited.keys():
                            if visited in tag and tags_visited[visited] >= self.MAX_VISITS_PER_TAG:
                                ignore_flag = True 
                                break

                        if not ignore_flag:
                            if tag in tags_visited:
                                tags_visited[tag] += 1
                            else:
                                tags_visited[tag] = 1

                            #print("calling model")
                            model_call_count += 1
                            print("Calling model on question: " + str(question) + ", context: ", str(tag))
                            result = self.question_answerer(question=question, context=tag)

                            score_to_add = result["score"] / num_searches * weight

                            if result["answer"] in results:
                                results[result["answer"]] += score_to_add
                            else:
                                results[result["answer"]] = score_to_add

        print("num times called model", model_call_count)
        print(results)
        answer = ""
        if results:
            answer = max(results, key=results.get)

        if ">" in answer:
            if m := re.findall(r">(.*)<?", answer):
                answer = m[0]
        if "<" in answer:
            if m := re.findall(r"(.*)<", answer):
                answer = m[0]

        print("Here's the answer:", answer)
        return answer


