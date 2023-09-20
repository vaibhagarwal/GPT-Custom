from langchain.chains import RetrievalQA
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
#from langchain.embeddings import HuggingFaceInstructEmbeddings
#from langchain.llms import HuggingFacePipeline
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from constants import CHROMA_SETTINGS, SOURCE_DIRECTORY, PERSIST_DIRECTORY
from transformers import LlamaTokenizer, LlamaForCausalLM, GenerationConfig, pipeline

from constants import CHROMA_SETTINGS



 

def main():
    # load the instructorEmbeddings
    embeddings = OpenAIEmbeddings(openai_api_key = "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" )
    # load the vectorstore
    db = Chroma(persist_directory=PERSIST_DIRECTORY, embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
    retriever = db.as_retriever()
    # Prepare the LLM
    callbacks = [StreamingStdOutCallbackHandler()]
    # load the LLM for generating Natural Language responses. 
    llm = ChatOpenAI(openai_api_key = "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")
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)
    # Interactive questions and answers
    while True:

        system_message="after providing answer to my question, provide a list of keywords in the answer with their respective meanings.\t"
        #system_message=""
        query = input("\nEnter a query: ")
        if query == "exit":
            break
        query=system_message+query
        # Get the answer from the chain
        res = qa(query)    
        answer, docs = res['result'], res['source_documents']

        # Print the result
        print("\n\n> Question:")
        print(query)
        print("\n> Answer:")
        print(answer)
        
        # # # Print the relevant sources used for the answer
        # print("----------------------------------SOURCE DOCUMENTS---------------------------")
        # for document in docs:
        #     print("\n> " + document.metadata["source"] + ":")
        #     print(document.page_content)
        # print("----------------------------------SOURCE DOCUMENTS---------------------------")


if __name__ == "__main__":
    main()