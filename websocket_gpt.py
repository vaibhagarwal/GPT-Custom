from aiohttp import web
from dotenv import load_dotenv
load_dotenv()#not required
from fuzzywuzzy import fuzz
from sentence_transformers import SentenceTransformer, util
import os
import openai 
openai.api_key="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"
openai.Model.list()#not required
import asyncio
import os
import json


#for 100% match
def find_best_matching_question(user_questions, user_input):
    best_match = None
    max_similarity = 0

    # Remove trailing punctuation from the reference question
    user_input = user_input.rstrip('.?')

    for user_question in user_questions:
        # Remove trailing punctuation from user question
        user_question_cleaned = user_question.rstrip('.?')

        similarity = fuzz.token_set_ratio(user_question_cleaned.lower(), user_input.lower())
        if similarity > max_similarity:
            max_similarity = similarity
            best_match = user_question

    if max_similarity >= 100:  # You can adjust the threshold as needed
        flag = 1
    else:
        flag = 0
    return best_match, flag

#for variations match 
def semantic_similarity_match(embeddings1, embeddings2, threshold=0.7):
    similarity_score = util.pytorch_cos_sim(embeddings1, embeddings2)[0][0]
    return similarity_score > threshold


#handles websocket communication with client
#allows you to write code that can perform multiple tasks concurrently without blocking the execution of other tasks.
async def chat(request):
    ws=web.WebSocketResponse() #initialising websocket response object 
    await ws.prepare(request) #preparing ws for comm.
    # particular operation should be awaited before moving on to the next step.
    #input questions list
    assistant_message=""
    user_questions = [
        "Show yourself",
        "Do you have any favorite quotes or sayings?",
        "How do you handle changes in your routine?",
        "What's a skill you wish you could master overnight?",
        "If you could meet any historical figure, who would it be and why?",
        "What's your idea of a perfect day?",
        "What's the most valuable lesson you've learned in life so far?",
        "How do you cope with loneliness, if at all?",
        "Are you more of a planner or do you prefer to go with the flow?",
        "What's something on your bucket list?",
        "What's your favorite way to exercise or stay active?",
        "How do you recharge when you're feeling drained?",
        "What's a topic or subject you're passionate about?",
        "What's the best gift you've ever received?",
        "How do you handle setbacks or failures?",
        "If you could possess any superpower, what would it be and why?",
        "What's the most interesting conversation you've had recently?",
        "How do you overcome self-doubt or insecurities?",
        "What's your favorite childhood story or memory?",
        "If you could give your younger self advice, what would it be?",
        "What is your name?",
        "What is edu?",
        "What is Residents medical?",
        "What is your age?",
        "Who is your favorite actor/actress?",
        "Are you Hannah?",
        "If you could have any superpower, what would it be and why?",
        "What's your favorite book/movie/TV show?",
        "What's the most interesting thing you've learned recently?",
        "Tell me some facts about you.",
        "Do you like talking to me?",
        "Which type of music do you like?",
        "How are you feeling today?",
        "Are you introvert or extrovert?",
        "Do you like socializing?",
        "How can you help me in my study?",
        "What is your favorite subject?",
        "How many students are in Class of 2027?",
        "Can you think on your own?",
        "What is the meaning of your name?",
        "Who is Dr. Michael Everest?",
        "Who created edyou?",
        "How can I download the presentation?"
    ]
    prompt = f"""As an incredibly helpful and detail-oriented assistant with remarkable intelligence, your primary role involves
        assisting users effectively. Your main objective is to skillfully identify the best-matched example from the list provided.
        In achieving this, focus on comprehending the intention and meaning of the question, while
        meticulously ensuring that entities such as 'his/her/him/you,' along with names of individuals and places, should be a precise
        match.In the scenario where the user's question aligns exactly with any of the provided examples and the entities match
        identically, your response should mirror the exact example in this format: 'Match: 'Insert Relevant Example Here.'
        Conversely, if no exact match exists, your responsibility shifts to addressing the user's query based on your own
        extensive knowledge.To illustrate, when the user inquires, 'which color do you like the most,' it should correspond
        with the example 'what is your favorite color.' However, if the user's query involves 'which color does she like the
        most,' no matching should occur.Presented below is the compilation of examples you should be working with: {user_questions}
        Kindly rememebr that you have to show the match only if it is in the list of given questions if not then answer form your own knowledge.
        Additionally, when the questions have words like 'you' or 'your,'
        remember that we're just looking for matches with the examples, not asking you questions unless there is no match found.
        Also note that you have to just give direct answer liek a human instead of giving any warning."""
    conversation=[{"role":"system","content":prompt}]
    
    async for msg in ws:# an async. loop
        if msg.type==web.WSMsgType.TEXT:
            if msg.data=='close':
                await ws.close()
            else:
                try:
                    data=json.loads(msg.data)#received data
                    print('Received:',data['content'])
                    user_input=data['content']
                    best_matched_question, flag = find_best_matching_question(user_questions, user_input)

                    if flag == 1:
                        print("100% match found\n")
                        response = f"Match found: {best_matched_question}" 
                        assistant_message += response
                        await ws.send_str(response)#sends the response string to the client through the WebSocket connection
                        ack = await ws.receive()#waits for a message to be received from the client through the WebSocket connection.

                        if ack.data != 'ack':
                            print("did not receive acknowledgement from client") #checks if the received message (stored in ack.data) is not equal to the string 'ack'. If it's not equal, it means that the acknowledgement from the client was not received successfully.
                                        #response_type = "semantic"
                    else:
                         # Load the pre-trained sentence transformer model
                        model = SentenceTransformer('distilbert-base-nli-stsb-mean-tokens')

                        reference_embedding = model.encode([user_input], convert_to_tensor=True)
                        for user_question in user_questions:
                            user_embedding = model.encode([user_question], convert_to_tensor=True)
                            if semantic_similarity_match(reference_embedding, user_embedding):
                                best_matched_question = user_question
                                flag = 1
                                break
                        
                        if flag == 1:
                            print("semantic match found\n")
                            response = f"Match found: {best_matched_question}"
                            assistant_message += response
                            await ws.send_str(response)
                            ack = await ws.receive()

                            if ack.data != 'ack':
                                print("did not receive acknowledgement from client")
                                                #response_type = "semantic"
                        else:
                            print("moving to gpt")
                            conversation.append({"role":"user","content":user_input})
                            response=openai.ChatCompletion.create(model="gpt-4",
                                                          messages=conversation,
                                                          max_tokens=100,
                                                          temperature=0.2,
                                                          stream=True)
                    
                    

                            for chunk in response:
                                content=chunk['choices'][0]['delta'].get('content','')
                                print(content)
                                assistant_message+=content
                                await ws.send_str(content)
                                ack=await ws.receive()

                                if ack.data!='ack':
                                    print("did not receive acknowledgement from client")

                                if chunk['choices'][0]['delta'].get('action')=='stop':
                                    conversation.append({"role":"assistant","content":assistant_message})
                                    assistant_message=""

                except Exception as e:
                    print('OpenAI API error:', e)

        elif msg.type==web.WSMsgType.ERROR:
            print('ws connection closed with exception %s' % ws.exception())
        
    print('websocket connection closed')

    return ws

async def server_static(request):   #used to serve the HTML file for the client-side interface.
    return web.FileResponse("E:\ed-you\streaming\clientside.html")

app=web.Application() #creates an instance of the aiohttp Application class, which will be used to define and manage the web application's routes and settings.
app.router.add_route('GET','/ws',chat) #dds a route to the application's router
app.router.add_route('GET','/',server_static)#dds a route to the root URL path ("/") that will be handled by the server_static coroutine function.

web.run_app(app,port=1888)#tarts the aiohttp web server and runs the application. It listens on port 1888 and serves the defined routes.


