from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
#from datauploader import BlobTools
#blob_tools = BlobTools()
university_info = {
    "https://www.salisbury.edu/": "salisbury_university_page"
    }
university_info_keys = list(university_info.keys())
loader = RecursiveUrlLoader(
    url=university_info_keys[0], max_depth=1, extractor=lambda x: Soup(x, "html.parser").text
)
pages = loader.load()

# i = current iteration, page = current page in pages
for i, page in enumerate(pages):
    # actual content on page
    page_content = page.page_content
    # metadata about page, url, title, description, etc.
    page_meta_data = page.metadata
    # getting the url associated with the page
    url = page_meta_data['source']
    # rename the page to {university_name_(i+1)}, i.e. 'salisbury_university_page_1'
    blob_name = f"{university_info[url]}_{i+1}"
    # upload the doc to the blob container
    # blob_tools.data_upload(blob_name, page_content, page_meta_data)
print(pages[0].metadata)

