from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from datauploader import BlobTools

# for checking robots.txt files
import requests
import urllib.robotparser

# BlobToos instance
blob_tools = BlobTools()


def download_robots_txt(university_url):
    response = requests.get(university_url + "/robots.txt")
    if response.status_code == 200:
        return response.text
    return None

def parse_robots_txt(robots_txt):
    disallowed_paths = set()
    lines = robots_txt.splitlines()
    for line in lines:
        if line.startswith('Disallow: '):
            path = line.split(': ')[1].lstrip('/')
            disallowed_paths.add(path)
        print(f"line: {line}")
    return disallowed_paths
    

# def should_scrape(university_url, user_agent, robots_txt):
#     if robots_txt is None:
#         return True
#     rp = urllib.robotparser.RobotFileParser()
#     rp.parse(robots_txt.splitlines())
    
#     return rp.can_fetch(user_agent, university_url)

def scraper(university_url, robots_txt):
    user_agent = "url@url.com, Azure CloudForce Track, spresley1@gulls.salisbury.edu, Admissions+DisabilityHelperScraper"
    disallowed_paths = parse_robots_txt(robots_txt)
    
    loader = RecursiveUrlLoader(
        url=university_url, max_depth=1, extractor=lambda x: Soup(x, "html.parser").text
    )
    
    pages = loader.load()
    for page in pages:
        # Extract path after root URL (https://www.school.edu/)
        path = page.url[len(university_url):]
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
    "https:": "salisbury_university_page"
    }

university_urls = list(university_info.keys())
for university_url in university_urls:
    robots_txt = download_robots_txt(university_url)
    robots_txt_url = university_url + "robots.txt"
    scraper(university, robots_txt)

