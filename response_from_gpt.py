import openai
openai.api_key = "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"
def ask_gpt(user_input):
    

    prompt = f""" You're a helpful assistant that gives answers to user questions effeciently. You shouldn't say
      'as an ai i don't know the answer to this question' or 'as of my last knowledge in september 2021 i don't know'. Just respond liek a normal human would do"""
    #for later you can catch september 2021 in resposne and respond other ways.


#
    messages = [{"role": "system", "content": prompt}]
    messages.append({"role": "user", "content": user_input})


    completion = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0.2,
        max_tokens=100,  # You can adjust the number of tokens as needed
        messages=messages
    )

    ans = completion['choices'][0]['message']['content']

    last_full_stop_position = ans.rfind(".")
    if last_full_stop_position != -1:
        final_response = ans[:last_full_stop_position + 1].strip()
    else:
        final_response=ans
        final_response = f"Getting response form GPT: {ans}"

    return final_response
