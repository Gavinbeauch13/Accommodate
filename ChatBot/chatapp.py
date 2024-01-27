import os
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from dotenv import load_dotenv


load_dotenv()

def run_conversation():
    llm = ChatOpenAI(model_name='gpt-3.5-turbo')
    conversational_chain = ConversationChain(llm=llm)
    conversation_history = []
    
    print("Hello! How may I help you?\n")
    
    while True:
        user_input = input("You:\n")
        
        # Add user input to conversation history
        conversation_history.append({"text": user_input, "is_usesr": True})
        
        # Get the models response
        model_response = conversational_chain.invoke(conversation_history)

        # Print the model response dictionary
        #print("Model response dictionary:\n", model_response)

        # Print model response and update chat history
        print("AI:\n", model_response["response"])
        conversation_history.append(model_response)

run_conversation()


