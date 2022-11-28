from typing import List, Dict
from rake_nltk import Rake
import re

class NLPModel:
    """ NLPModel object that uses a question_answerer model """

    def __init__(self, question_answerer):
        """ Initializes a NLPModel object with a model input"""
        self.raker = Rake()
        self.max_searches = 32
        self.question_answerer = question_answerer

    def get_keywords(self, question: str, n: int = 1):
        self.raker.extract_keywords_from_text(question)
        return str(self.raker.get_ranked_phrases()[0]).split(" ")

    def product_question(self, tags: List[str], question: str):
        """ get all tags of soup """
        results: Dict[str, int] = {}
        # max_answer represents the answer with the highest confidence
        keywords = self.get_keywords(question, 10)
        print(keywords)
        search = 1
        tags_visited = {}
        tags = [tag for tag in tags if len(tag) < 700]
        print("Starting the algorithm")
        for tag in tags:
            if search > self.max_searches:
                break

            contain = False
            weight = 0
            for word in keywords:
                if word in tag:
                    contain = True
                    weight += 1

            if contain:

                ignore_flag = True
                for visited in tags_visited.keys():
                    if visited in tag and tags_visited[visited] >= 2:
                        ignore_flag = False
                        break

                if ignore_flag:
                    if tag in tags_visited:
                        tags_visited[tag] += 1
                    else:
                        tags_visited[tag] = 1

                    result = self.question_answerer(question=question, context=tag)

                    if result["answer"] in results:
                        results[result["answer"]] += result["score"] / search * weight
                    else:
                        results[result["answer"]] = result["score"] / search * weight

                    search += 1
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
