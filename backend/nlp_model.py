import collections
import re
from typing import List, Dict

from backend.timer import timed

class NLPModel:
    """ NLPModel object that uses a question_answerer model """

    def __init__(self, question_answerer):
        """ Initializes a NLPModel object with a model input"""

        self.question_answerer = question_answerer

        self.min_tag_length = 0
        self.max_tag_length = 1000

    @timed
    def product_question(self, tags: List[str], keyword: str):
        """ get all tags of soup """
        results: Dict[str, int] = {}
        question = "What is " + keyword + "?"
        # max_answer represents the answer with the highest confidence
        (max_answer, max_confidence) = ("", 0)
        # answer list will be used to find the most commonly produced answer by qa model
        answer_list = []
        for tag in tags:
            if keyword in tag and len(tag) < self.max_tag_length:
                result = self.question_answerer(question=question, context=tag)

                answer_list.append(result["answer"])
                if result["answer"] not in results:
                    results[result["answer"]] = result["score"]
                else:
                    results[result["answer"]] += result["score"]

                if result["score"] > max_confidence:
                    (max_answer, max_confidence) = (result["answer"],
                                                    result["score"])

        answer_common = ""
        if len(answer_list) != 0:
            answer_common = collections.Counter(answer_list).most_common(1)[0][0]

        # answer_sum_confidences represents the answer with the highest sum of confidences

        answer_sum_confidences = ""
        if results:
            answer_sum_confidences = max(results, key=results.get)
        # max_value = results[answer_sum_confidences]

        # heuristic to check if answers from above are consistent with
        # each other as the most common answer provided by the algorithm
        answers = [max_answer, answer_common, answer_sum_confidences]
        final_answer = collections.Counter(answers).most_common(1)[0][0]
        match = re.search(r"[0-9][0-9]*.?[0-9]?", final_answer)

        if match:
            return match.group()
        return self.correction(results)

    @staticmethod
    def correction(results: Dict[str, int]):
        """ correction method """
        for k, _ in results.items():
            match = re.search(r"[0-9][0-9]*.?[0-9]?", k)
            if match:
                return match.group()

        return ""
