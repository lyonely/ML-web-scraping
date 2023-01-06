from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re 

def has_numbers(input_string):
    return bool(re.search(r'\d', input_string))


def get_answer_similarity(output_ans, correct_ans):
    ##idea: if both answers contain numbers, first check if the 
    # nubers are the same, if they are not return 0
    if has_numbers(output_ans) and has_numbers(correct_ans):
        output_nums = re.findall(r'\d+', output_ans)
        correcrt_nums = re.findall(r'\d+', correct_ans)
        if  set(output_nums) != set(correcrt_nums):
            return 0

    #next, do transformer logic
    sentences = [output_ans, correct_ans]
    model_name = 'bert-base-nli-mean-tokens'
    model = SentenceTransformer(model_name)
    sentence_vecs = model.encode(sentences)
    out = cosine_similarity(
        [sentence_vecs[0]],
        sentence_vecs[1:]
        )
    return out 