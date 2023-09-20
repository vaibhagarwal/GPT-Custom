import re
#to check of localgpt says i dont know the answer

def find_if_no_response(gpt_response):
    flag = 1
    # for possible_answer in possible_answers:
    #     # Define a list of keywords/patterns that indicate a lack of knowledge
    keywords = ["don't know", "not sure", "no access", "cannot answer", "no information","I don't know", "does not mention"]

    # Check if any of the keywords/patterns are present in the response
    for keyword in keywords:
        if re.search(keyword, gpt_response, re.IGNORECASE):
            flag = 0
            # return flag
    return flag