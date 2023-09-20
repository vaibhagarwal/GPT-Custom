import pandas as pd
import openai
import re
import json

openai.api_key = "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"

questions=[ 
    "What is your favorite color?",
    "How do you like to spend your weekends?"
    ]
df=[]

# Loop through each question and extract attributes and synonyms
for question in questions:
    prompt = f"""Generate all possible variations of question '{question}' and extract all keywords from those variations. provide the answer as keywords=[]"""
    messages = [{"role": "system", "content": prompt}, {"role": "user", "content": question}]

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0.2,  
        messages=messages
    )

    response = completion['choices'][0]['message']['content']

    # Use regular expression to extract keywords
    keywords_match = re.search(r'Keywords:\s\[(.*?)\]', response)

    if keywords_match:
        keywords_text = keywords_match.group(1)  # Get the text inside square brackets
        keywords_list = re.findall(r'\b\w+\b', keywords_text)  # Extract individual keywords

        answer = f"responding to question: {question}"
        
        # Append data as a dictionary to the list
        df.append({'questions': question, 'answer': answer, 'attributes': keywords_list})
    
    # Save the list of dictionaries as a JSON file
with open('output.json', 'w') as json_file:
    json.dump(df, json_file, indent=4)

print("Data has been saved as 'output.json'.")