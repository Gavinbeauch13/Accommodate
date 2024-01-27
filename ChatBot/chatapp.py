import os
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from dotenv import load_dotenv


load_dotenv()

class chat_bot:
    def __init__(self):
        self.llm = ChatOpenAI(model_name='gpt-3.5-turbo')
        self.conversational_chain = ConversationChain(llm=self.llm)
        self.conversation_history = []            
        self.user_input = ""
            
    def run_conversation(self, user_input)->str:    
        print("Hello! How may I help you?\n") 
        
        self.user_input = user_input
            
        # Add user input to conversation history
        self.conversation_history.append({"text": user_input, "is_user": True})
            
        # Get the models response

        model_response = self.conversational_chain.invoke(self.conversation_history)

        # Print the model response dictionary
        #print("Model response dictionary:\n", model_response)

        # Print model response and update chat history
        response = "AI:\n," + model_response["response"]
        self.conversation_history.append(model_response)
        return response

    #run_conversation()





