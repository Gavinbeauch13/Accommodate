from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from datauploader import BlobTools

# for checking robots.txt files
import requests
import urllib.robotparser

# BlobToos instance
blob_tools = BlobTools()


def download_robots_txt(robots_txt_url):
    response = requests.get(robots_txt_url)
    if response.status_code == 200:
        return response.text
    return None

def parse_robots_txt(robots_txt, disallowed_paths):
    #disallowed_paths = set()
    lines = robots_txt.splitlines()
    for line in lines:
        if line.startswith('Disallow: '):
            path = line.split(': ')[1].lstrip('/')
            disallowed_paths.add(path)
        print(f"line: {line}, path_PRT: {path}")
    return disallowed_paths
    

# def should_scrape(university_url, user_agent, robots_txt):
#     if robots_txt is None:
#         return True
#     rp = urllib.robotparser.RobotFileParser()
#     rp.parse(robots_txt.splitlines())
    
#     return rp.can_fetch(user_agent, university_url)

def scraper(university_url, robots_txt):
    disallowed_paths = set()
    parse_robots_txt(robots_txt, disallowed_paths)
    print(f"Disallowed Paths: {disallowed_paths}")
    
    loader = RecursiveUrlLoader(
        url=university_url, max_depth=1, extractor=lambda x: Soup(x, "html.parser").text
    )
    
    print(f"loader_SCRAPER: {loader}")
    pages = loader.load()
    print(f"pages_SCRAPER: {pages}")
    
    for page in pages:
        # Extract path after root URL (https://www.school.edu/)
        path = page.url[len(university_url):]
        print(f"Path_SCRAPER = {path}")
        if path not in disallowed_paths:
            upload_page(page)

def upload_page(pages):
    # i = current iteration, page = current page in pages
    for i, page in enumerate(pages):
        print("starting upload on {page}, iteration: {i}")
        # actual content on page
        page_content = page.page_content
        # metadata about page, url, title, description, etc.
        page_metadata = page.metadata
        # getting the url associated with the page
        url = page_metadata['source']
        # rename the page to {university_name_(i+1)}, i.e. 'salisbury_university_page_1'
        blob_name = f"{university_info[url]}_{i+1}"
        # upload the doc to the blob container
        blob_tools.data_upload(blob_name, page_content, page_metadata)
        print(f"Done uploading Page: {page}")
    print("all pages uploaded")
    print(f"Following pages metadata was not uploaded, {blob_tools.oversized_metadata.keys()}")
    
university_info = {
    "https://www.umbc.edu/": "umbc_page", 
    "https://www.vt.edu/": "vt_page", 
    "https://www.hopkins.edu/": "hopkins_page",
    }

university_urls = list(university_info.keys())
for university_url in university_urls:
    robots_txt_url = university_url + "robots.txt" 
    robots_txt = download_robots_txt(robots_txt_url)
    scraper(university_url, robots_txt)

