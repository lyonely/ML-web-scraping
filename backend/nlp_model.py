from typing import List, Dict
import re
from rake_nltk import Rake
import requests


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
                for visited, item in tags_visited.items():
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
