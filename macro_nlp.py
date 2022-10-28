from webscraper import get_soup
import collections
import re
from transformers import pipeline
question_answerer = pipeline("question-answering", model="deepset/roberta-base-squad2")
# q/a pipeline set up with the "deepset/roberta-base-squad2" model
# https://huggingface.co/deepset/roberta-base-squad2


def product_macro(product_url, macro):
    # get all tags of soup
    gs = get_soup(product_url).find_all()
    results = {}

    macro = str(macro).strip().lower()
    question = "What is " + macro + "?"

    # max_answer represents the answer with the highest confidence
    (max_answer, max_confidence) = ("", 0)

    # answer list will be used to find the most commonly produced answer by qa model
    answer_list = []

    for tag in gs:
        tag = str(tag).strip().lower()
        if macro in tag and 40 < len(tag) < 1000:
            result = question_answerer(question=question, context=tag)
            # result = { "answer": ..., "score": ..., ... }
            answer_list.append(result["answer"])
            if result["answer"] not in results:
                results[result["answer"]] = result["score"]
            else:
                results[result["answer"]] += result["score"]

            if result["score"] > max_confidence:
                (max_answer, max_confidence) = (result["answer"], result["score"])

    most_common = collections.Counter(answer_list).most_common(1)[0][0]

    # answer_sum_confidences represents the answer with the highest sum of confidences
    max_value = 0
    answer_sum_confidences = ""
    for k,v in results.items():
        if max_value < v:
            max_value = v
            answer_sum_confidences = k

    # heuristic to check if answers from above are consistent with
    # each other as the most common answer provided by the algorithm
    answers = [max_answer, most_common, answer_sum_confidences]

    final_answer = collections.Counter(answers).most_common(1)[0][0]

    match = re.search(r"[0-9]*g", final_answer)
    if match:
        return final_answer
    else:
        return correction(results)


# this method is very hacky, and it won't work on the edge case where there is no mass in the
# results table as is the case with "https://www.tesco.com/groceries/en-GB/products/268414699"
def correction(results):
    s = ""
    for k, v in results.items():
        s += k + " is the mass, "
    result = question_answerer(question="What is mass in grams?", context=s)
    return result["answer"]
