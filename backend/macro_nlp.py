import collections
import re
from typing import Dict, List
from transformers import pipeline

from rake_nltk import Rake
import nltk 
import itertools


question_answerer = pipeline("question-answering",
                             model="deepset/roberta-base-squad2")

# q/a pipeline set up with the "deepset/roberta-base-squad2" model
# https://huggingface.co/deepset/roberta-base-squad2


def get_keywords(question: str, n: int) -> List[str]:
    #returns top n key words form the question
    r = Rake()
    r.extract_keywords_from_text(question)
    return list(itertools.chain.from_iterable(map(lambda x : x.split(), r.get_ranked_phrases())))[:n]


#pylint: disable-next=too-many-locals
def product_question(tags: List[str], question: str):
    """ get all tags of soup """
    results: Dict[str, int] = {}

    question_key_words = get_keywords(question, 5)

    # max_answer represents the answer with the highest confidence
    (max_answer, max_confidence) = ("", 0)
    # answer list will be used to find the most commonly produced answer by qa model
    answer_list = []

    for tag in tags:
        if any(key_word in tag for key_word in question_key_words) and 40 < len(tag) < 1000:
            result = question_answerer(question=question, context=tag)
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
    max_value = 0
    answer_sum_confidences = ""
    for key, value in results.items():
        if max_value < value:
            max_value = value
            answer_sum_confidences = key

    # heuristic to check if answers from above are consistent with
    # each other as the most common answer provided by the algorithm
    answers = [max_answer, answer_common, answer_sum_confidences]
    final_answer = collections.Counter(answers).most_common(1)[0][0]

    match = re.search(r"[0-9][0-9]*.?[0-9]?g", final_answer)
    if match:
        return match.group()
    return correction(results)


# this method is very hacky, and it won't work on the edge case where there is no mass in the
# results table as is the case with "https://www.tesco.com/groceries/en-GB/products/268414699"
def correction(results: Dict[str, int]):
    """ correction method """
    for k, _ in results.items():
        match = re.search(r"[0-9][0-9]*.?[0-9]?g", k)
        if match:
            return match.group()

    return ""
