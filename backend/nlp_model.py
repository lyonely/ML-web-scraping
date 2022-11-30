from typing import List, Dict
from rake_nltk import Rake
import re

class NLPModel:
    """ NLPModel object that uses a question_answerer model """

    def __init__(self, question_answerer):
        """ Initializes a NLPModel object with a model input"""
        self.raker = Rake()
        self.question_answerer = question_answerer
        self.MAX_SEARCHES = 32
        self.NUM_KEYWORDS = 10
        self.MAX_TAG_LENGTH = 700
        self.MAX_VISITS_PER_TAG = 2
    

    

    def get_keywords(self, question: str, n: int = 1):
        self.raker.extract_keywords_from_text(question)
        return str(self.raker.get_ranked_phrases()[0]).split(" ")[:n]
    

    def product_question(self, tags: List[str], question: str):
        """
        IDEAS TO REDUCE THE NUMBER OF TIMES WE CALL THE MODEL

        1. make contain more strict (maybe a certain percentage has to contain the words?)
        2. make tags a shorter list - self.MAX_TAG_LENGTH can be shorter
        3. shouldn't we remove all the html from visited? ie just be left with the text
        4. make numsearches shorter
        5. maybe tune max_searches depending on type of website
        
        """
        """ get all tags of soup """
        results: Dict[str, int] = {}
        # max_answer represents the answer with the highest confidence
        keywords = self.get_keywords(question, self.NUM_KEYWORDS)
        print(keywords)
        tags_visited = {}
        tags = [tag for tag in tags if len(tag) < self.MAX_TAG_LENGTH]
        print("Starting the algorithm")
        model_call_count = 0
        num_searches = 1

        # sorted_tags = sorted(tags, key = len)
        sorted_tags = tags

        #idea: join tags together so that we call the model less times
        max_tag_length = 100
        loop_tags = []
        curr = ""
        i = 0
        while i < len(sorted_tags):
            while(len(curr) < max_tag_length and i < len(sorted_tags)):
                curr = curr + sorted_tags[i]
                i += 1
            loop_tags.append(curr)
            curr = ""

        print("loop tags length", len(loop_tags))
        print("tags length", len(tags))
        for tag in sorted_tags:
            if num_searches > self.MAX_SEARCHES:
                break
            word_map = [word in tag for word in keywords]
            contain = any(word_map)
            weight = sum(word_map) * 0.5

            if contain:
                    ignore_flag = False
                        

                    for visited in tags_visited.keys():
                        text_tag = re.sub("\<.*?\>", "", tag)
                        if (visited in text_tag or text_tag in visited) and tags_visited[visited] >= self.MAX_VISITS_PER_TAG:
                            ignore_flag = True 
                            break

                    if not ignore_flag:
                        if tag in tags_visited:
                            tags_visited[tag] += 1
                        else:
                            tags_visited[tag] = 1


                        #print("calling model")
                        model_call_count += 1
                        print("Calling model on question: " + str(question) + ", context: ", str(tag))
                        result = self.question_answerer(question=question, context=tag)
                        score_to_add = result["score"] / num_searches * weight

                        if result["answer"] in results:
                            results[result["answer"]] += score_to_add
                        else:
                            results[result["answer"]] = score_to_add

        




        print("num times called model", model_call_count)
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


    def product_question_prime(self, tags: List[str], question: str):
        
        """ get all tags of soup """
        results: Dict[str, int] = {}
        # max_answer represents the answer with the highest confidence
        keywords = self.get_keywords(question, self.NUM_KEYWORDS)
        print(keywords)
        tags_visited = {}
        tags = [tag for tag in tags if len(tag) < self.MAX_TAG_LENGTH]
        print("Starting the algorithm")
        model_call_count = 0
        for tag in tags:
            word_map = [word in tag for word in keywords]
            contain = any(word_map)
            weight = sum(word_map)

            if contain:
                for num_searches in range(1, self.MAX_SEARCHES +1):
                        ignore_flag = False
                        

                        for visited in tags_visited.keys():
                            if visited in tag and tags_visited[visited] >= self.MAX_VISITS_PER_TAG:
                                ignore_flag = True 
                                break

                        if not ignore_flag:
                            if tag in tags_visited:
                                tags_visited[tag] += 1
                            else:
                                tags_visited[tag] = 1

                            #print("calling model")
                            model_call_count += 1
                            print("Calling model on question: " + str(question) + ", context: ", str(tag))
                            result = self.question_answerer(question=question, context=tag)

                            score_to_add = result["score"] / num_searches * weight

                            if result["answer"] in results:
                                results[result["answer"]] += score_to_add
                            else:
                                results[result["answer"]] = score_to_add

        




        print("num times called model", model_call_count)
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


