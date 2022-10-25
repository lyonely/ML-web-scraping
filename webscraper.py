import json
import sys
import collections
from util import get_soup
from transformers import pipeline
question_answerer = pipeline("question-answering", model="deepset/roberta-base-squad2")

def all_products_macros(url, macro):
    soup = get_soup(url)
    products = set()

    try:
        links = soup.select('a')
        for link in links:
            to_scrape = 'https://www.tesco.com' + str(link.get('href'))
            if '/products/' in to_scrape:
                products.add(to_scrape)

    except Exception:
        raise Exception("Error while reading CSS selector")


    product_to_macro = {}
    for product in products:
        answer = product_macro(product, macro)
        print(answer)
        product_to_macro[product] = answer

    json_object = json.dumps({
        "search_query" : url,
        "products_to_macro": product_to_macro
    })

    return json_object


def product_macro(product_url, macro):
    macro = str(macro).strip().lower()
    gs = get_soup(product_url).find_all()
    confidence = 0
    answer_highest_confidence = ""
    results = {}
    for tag in gs:
        tag = str(tag)
        if macro in tag.strip().lower() and 1000 > len(tag) > 40:
            q = "What is " + str(macro)
            result = question_answerer(question=q, context=tag)
            if result["answer"] not in results:
                results[result["answer"]] = result["score"]
            else:
                results[result["answer"]] += result["score"]

            if result["score"] > confidence:
                confidence = result["score"]
                answer_highest_confidence = result["answer"]

    answer_counter = collections.Counter(results).most_common(1)[0][0]

    max_value = 0
    answer_sum_confidences = ""
    for k,v in results.items():
        if v > max_value:
            max_value = v
            answer_sum_confidences = k

    # heuristic to check if answers from above are consistent with each other
    # as the most common answer provided by the algorithm
    answers = [answer_counter, answer_sum_confidences, answer_highest_confidence]
    final_answer = collections.Counter(answers).most_common(1)[0][0]
    return final_answer


def main(url, macro):
    print(all_products_macros(url, macro))


if __name__ == "__main__":
    # python3 webscrape.py "https://www.tesco.com/groceries/en-GB/shop/fresh-food/all" "fat"
    main(sys.argv[1], sys.argv[2])