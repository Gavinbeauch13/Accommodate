import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
#from azure.ai.textanalytics import TextAnalyticsClient
from langchain_openai import AzureChatOpenAI
#from langchain.chains import ConversationChain
from dotenv import load_dotenv
from openai import AzureOpenAI
#from langchain.chat_models import AzureChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

load_dotenv()

class chat_bot:
    def __init__(self):
        #self.llm = ChatOpenAI(model_name='gpt-3.5-turbo')
        self.llm = AzureChatOpenAI(
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            model_name="gpt-35-turbo",
            api_version="2023-12-01-preview",
            api_key=os.getenv("AZURE_OPENAI_KEY")
        )
        
        self.messages = [
            SystemMessage(content="You are a helpful assistant who aids high school students applying for college/university, specifically the universities of University of Baltimore City, Virginia Tech, and University of Delaware. You will use the extra data made available to you to answer questions regarding all aspects of admission, especially focusing on disability resources. You'll also use the resources available to you to answer questions regarding student experience at a given college.")
        ]
        
        self.search_url = os.getenv("AZURE_SEARCH_SERVICE_URL")
        self.search_key = os.getenv("AZURE_SEARCH_ADMIN_KEY")
        self.index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
        #self.conversational_chain = ConversationChain(llm=self.llm)
        self.conversation_history = []            
        self.user_input = ""
        
    #def make_query(self):
        
    def get_client(self):
        client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_KEY"),  
            api_version="2023-12-01-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
        )
        return client
    
    def get_deployment_name(self):
        deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        
        return deployment_name
    
    def search_documents(self, query):
        credential = AzureKeyCredential(self.search_key)
        client = SearchClient(endpoint=self.search_url, 
                              index_name=self.index_name,
                              credential=credential
                              )
        results = client.search(search_text=query, include_total_count=True)
        return [result for result in results]

    def run_conversation(self, user_input)->str:    
        self.messages.append(HumanMessage(content=user_input))

        # Search in the Azure index
        search_results = self.search_documents(user_input)
        
        if search_results:
            # Extract key information from the search results
            key_info = self.extract_key_information(search_results[0])

            # Check if key information is extracted
            if key_info:
                # Generate an informed response using the key information
                informed_response = f"Based on the latest information in our database, {key_info.get('description', 'the requested information is not available')}."
                self.messages.append(SystemMessage(content=informed_response))
            else:
                # If key information is not found, use a direct quote from the index
                direct_quote = search_results[0].get("content", "I couldn't find specific details in our database.")
                informed_response = f"Here's what I found in our database: {direct_quote}"
                self.messages.append(SystemMessage(content=informed_response))
        else:
            # If no search results, default to the AI model's general knowledge
            informed_response = "I couldn't find specific details in our database. However, based on my current knowledge..."

        # Generate AI model response
        model_response = self.llm.invoke(self.messages)
        self.messages.append(model_response)

        return model_response.content
    def extract_key_information(self, search_result):
        # Extracting specific information from the search result based on the fields in your index
        extracted_info = {}

        # Example: Extracting tuition cost
        # Assuming 'tuition_cost' is a field in your indexed documents
        if 'tuition_cost' in search_result:
            extracted_info['tuition_cost'] = search_result['tuition_cost']

        # Example: Extracting admission deadlines
        # Assuming 'admission_deadlines' is a field in your indexed documents
        if 'admission_deadlines' in search_result:
            extracted_info['admission_deadlines'] = search_result['admission_deadlines']

        # Example: Extracting program details
        # Assuming 'program_details' is a field in your indexed documents
        if 'program_details' in search_result:
            extracted_info['program_details'] = search_result['program_details']

        return extracted_info


    #run_conversation()
chat = chat_bot()
print(chat.run_conversation("Use your search query to find <<virginia tech tuition>> for the 2023-2024 year"))




