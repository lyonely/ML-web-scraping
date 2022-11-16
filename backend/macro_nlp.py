from transformers import pipeline
from rake_nltk import Rake
import itertools
import collections
from typing import List, Dict
import re


#takes in a question_answerer
#
class MacroNLP:

    def __init__(self, question_answerer):

        self.question_answerer = question_answerer

        # self.question_answerer = pipeline("question-answering",
        #                      model="deepset/roberta-base-squad2")

        # self.question_answerer_distil = pipeline("question-answering",
        #                      model = "distilbert-base-uncased")
        
        self.rake = Rake()

        self.MIN_TAG_LENGTH = 40
        self.MAX_TAG_LENGTH = 1000

    
    def get_keywords(self, question: str, n : int):
    #returns top n key words from the question
            r = Rake()
            r.extract_keywords_from_text(question)
            return list(itertools.chain.from_iterable(map(lambda x : x.split(), r.get_ranked_phrases())))[:n]
    

    def product_question(self, tags: List[str], question: str):
        """ get all tags of soup """
        results: Dict[str, int] = {}

        question_key_words = self.get_keywords(question, 5)

        # max_answer represents the answer with the highest confidence
        (max_answer, max_confidence) = ("", 0)
        # answer list will be used to find the most commonly produced answer by qa model
        answer_list = []

        for tag in tags:
            if any(key_word in tag for key_word in question_key_words) and self.MIN_TAG_LENGTH < len(tag) < self.MAX_TAG_LENGTH:
                result = self.question_answerer(question=question, context=tag)
                # result = { "answer": ..., "score": ..., ... }

                answer_list.append(result["answer"])
                if result["answer"] not in results:
                    results[result["answer"]] = result["score"]
                else:
                    results[result["answer"]] += result["score"]

                if result["score"] > max_confidence:
                    (max_answer, max_confidence) = (result["answer"],
                                                    result["score"])
        
        answer_common = collections.Counter(answer_list).most_common(1)[0][0]

        # answer_sum_confidences represents the answer with the highest sum of confidences
        answer_sum_confidences = ""
        answer_sum_confidences = max(results, key = results.get)
        max_value = results[answer_sum_confidences]

        # heuristic to check if answers from above are consistent with
        # each other as the most common answer provided by the algorithm
        answers = [max_answer, answer_common, answer_sum_confidences]
        final_answer = collections.Counter(answers).most_common(1)[0][0]

        match = re.search(r"[0-9][0-9]*.?[0-9]?g", final_answer)
        if match:
            return match.group()
        return self.correction(results)
    



    def correction(self, results: Dict[str, int]):
        """ correction method """
        for k, _ in results.items():
            match = re.search(r"[0-9][0-9]*.?[0-9]?g", k)
            if match:
                return match.group()

        return ""