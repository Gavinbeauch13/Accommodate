from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os
from dotenv import load_dotenv
import pickle

load_dotenv()

class BlobTools:
    """
    Class to check if a blob exists, if it doesn't create it and upload data
    """
    def __init__(self):
        # evironment variables
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        self.container_client = self.blob_service_client.get_container_client(self.container_name)
        
        # dictionary to keep track of any pages whos metadata is too large
        # key = page_name, value = page_metadata 
        self.oversized_metadata = {}
        
    def get_oversized_metadata(self)->dict:
        return self.oversized_metadata
       
    def validate_metadata_size(self, blob_name, page_metadata)->bool:
        """
            Args:
                page_name: name of page
                page_metadata: metadata for the page associated with page_name
            Returns:
                True if the metadata is within the size limits, False if it is too large
            If the metadata is too large, it is added to the oversized_metadata dictionary
            The blob_name is added as the key and the page_metadata as the value
            blob_name is the page's string contents in bytes in the form of a .txt file
        """   # get size of the pages metadata
        size_of_metadata = len(pickle.dumps(page_metadata))
        
        # if it's within the size limits (8kb) just return
        if size_of_metadata <= 8192:
            return True
        
        # if the meta data is too large add that page and it's metadata to oversized_metadata
        self.oversized_metadata[blob_name] = page_metadata
        return False
        # raise error if metadata is too large
        # raise ValueError("Metadata size is too large, adding to dictionary and continuing")

    
    def data_upload(self, page_name, page_content, page_metadata)->str:
        """
            Uploads data to Azure Blob Storage. If the blob does not exist, it is created as an append blob.
            Then, school_data is appended to the blob

            :param school_name: The name of the school, used to create blob name.
            :param school_data: Data to be uploaded
        """
        blob_name = f"{page_name}.txt"
        blob_client = self.container_client.get_blob_client(blob=blob_name)
        page_data_bytes = page_content.encode('utf-8')
        # Check if the blob exists, if it doesn't create it
        if not blob_client.exists():
            blob_client.create_append_blob()
        page_content = page_content.replace('\u2019', "'")
        page_metadata = {k.replace('\u2019', "'"): v.replace('\u2019', "'") if isinstance(v, str) else v for k, v in page_metadata.items()}
        # append data to blob
        blob_client.append_block(page_data_bytes)
        page_status = f"Page content for {page_name} was appended to storage container\nblob_client: {blob_client}, blob_name: {blob_name}"
        metadata_status = ""
        
        # new line for readability when debugging in terminal
        print("\n")
        # validate metadata is within size limits, if it is upload it, if it isn't skip it
        if self.validate_metadata_size(blob_name, page_metadata):
            blob_client.set_blob_metadata(metadata=page_metadata)
            metadata_status = f"page_metadata:\n{page_metadata}\nfor {page_name} were appended to blob: {blob_name}"
            return page_status, metadata_status
        metadata_status = f"Page content for {page_name} was appended to blob but page_metadata was too large and wasn't appended"
        return page_status, metadata_status
    
    