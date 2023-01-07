from typing import List, Dict
import re
from rake_nltk import Rake
from transformers import pipeline


class NLPModel:
    """ NLPModel object that uses a question_answerer model """

    def __init__(self):
        """ Initializes a NLPModel object with a model input"""
        self.rake = Rake()
        self.max_searches = 32
        model_name = "deepset/roberta-base-squad2"
        self.model_link = pipeline("question-answering", model=model_name)

    def get_keywords(self, question: str, num: int):
        """ Extracts relevant keywords from question """
        self.rake.extract_keywords_from_text(question)
        try:
            return str(self.rake.get_ranked_phrases()[0]).split(" ")[:num]
        except IndexError:
            return []

    # pylint: disable-next=too-many-locals, too-many-branches
    def product_question(self, tags: List[str], question: str):
        """ get all tags of soup """
        results: Dict[str, int] = {}
        # max_answer represents the answer with the highest confidence
        keywords = set(self.get_keywords(question, num=3))
        search = 1
        weight = 1
        tags_visited = {}
        tags = [tag for tag in tags if len(tag) < 700]
        for tag in tags:
            if search > self.max_searches:
                break

            contain = int(len(keywords) == 0)
            weight = 0 + int(contain)
            for word in keywords:
                if word in tag:
                    contain = True
                    weight += 0.5

            if contain:

                ignore_flag = True
                for visited, item in tags_visited.items():
                    if visited in tag and item >= 2:
                        ignore_flag = False
                        break

                if ignore_flag:
                    if tag in tags_visited:
                        tags_visited[tag] += 1
                    else:
                        tags_visited[tag] = 1
                    result = self.model_link(question, tag)

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
