import collections
import re
from typing import List, Dict
from rake_nltk import Rake
import itertools
# nltk.download('woquiet=True)


def get_keywords(question: str, n: int):
    r = Rake()
    r.extract_keywords_from_text(question)
    return list(itertools.chain.from_iterable(map(lambda x: x.split(), r.get_ranked_phrases())))[:n]


class NLPModel:
    """ NLPModel object that uses a question_answerer model """

    def __init__(self, question_answerer):
        """ Initializes a NLPModel object with a model input"""

        self.question_answerer = question_answerer

    def product_question(self, tags: List[str], question: str):
        """ get all tags of soup """
        results: Dict[str, int] = {}

        # max_answer represents the answer with the highest confidence
        (max_answer, max_confidence) = ("", 0)
        keywords = get_keywords(question, 10)
        search = 1
        max_searches = 2**32
        tags_visited = {}

        for tag in tags:
            if search > max_searches:
                break

            ignore_flag = True
            for visited in tags_visited.keys():
                if visited in tag and tags_visited[visited] >= 2:
                    ignore_flag = False
                    break

            contain = False
            for word in keywords:
                if word in tag:
                    contain = True
                    break

            if contain and ignore_flag and 30 < len(tag) < 400:
                s = re.findall(r'>(.+?)<', tag)
                context = " ".join(s)
                if context == "":
                    continue
                result = self.question_answerer(question=question, context=context)

                if result["answer"] in results:
                    results[result["answer"]] += result["score"] / search
                else:
                    results[result["answer"]] = result["score"] / search

                search *= 2

                if tag in tags_visited:
                    tags_visited[tag] += 1
                else:
                    tags_visited[tag] = 1

        print(search)
        # answer_sum_confidences represents the answer with the highest sum of confidences

        answer_sum_confidences = ""
        if results:
            answer_sum_confidences = max(results, key=results.get)

        # heuristic to check if answers from above are consistent with
        # each other as the most common answer provided by the algorithm
        # return self.question_answerer(question=question, context=answer_sum_confidences)["answer"]
        return answer_sum_confidences
        # print(self.correction(results))
        # return self.correction(results)

    @staticmethod
    def correction(results: Dict[str, int]):
        return list(dict(sorted(results.items(), key=lambda i: i[1], reverse=True)).keys())[0]
