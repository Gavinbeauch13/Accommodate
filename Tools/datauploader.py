from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()

class BlobTools:   
    """
    Class to check if a blob exists, if it doesn't create it and upload data
    """
    def __init__(self):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
        
    def data_upload(self, page_name, page_data):
        """
            Uploads data to Azure Blob Storage. If the blob does not exist, it is created as an append blob.
            Then, school_data is appended to the blob

            :param school_name: The name of the school, used to create blob name.
            :param school_data: Data to be uploaded
        """  
        blob_name = f"{page_name}.txt"
        blob_client = self.container_client.get_blob_client(blob=blob_name)
        
        page_data_bytes = page_data.encode('utf-8')
        # Check if the blob exists, if it doesn't create it
        if not blob_client.exists():
            blob_client.create_append_blob()
            
        # append data to blob
        blob_client.append_block(page_data_bytes)
        print(f"Data appended to blob: {blob_name}")
        
    
    
    