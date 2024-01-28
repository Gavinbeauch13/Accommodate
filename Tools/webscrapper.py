from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader
from datauploader import BlobTools

# for checking robots.txt files
import requests
import urllib.robotparser

# BlobToos instance
blob_tools = BlobTools()

# downloads all the disallowed URL extnesions
def download_robots_txt(robots_txt_url):
    # makes http call to get the robots.txt file
    response = requests.get(robots_txt_url)
    # if the response is 200, then it was a success, return the text of the robots.txt file
    if response.status_code == 200:
        return response.text
    # else it couldn't find or access the robots.txt file and returns None
    return None

# parses the robots.txt file and adds the disallowed paths into the disallowed_paths set
def parse_robots_txt(robots_txt, disallowed_paths, university_url):
    lines = robots_txt.splitlines()
    for line in lines:
        if line.startswith('Disallow: '):
            # remove the 'Disallow: ' from the line and remove any leading or trailing slashes
            # this is because when we check if a path is disallowed, we remove any leading or trailing slashes
            # from the path and check if it is in the disallowed_paths set
            path = line.split(': ')[1].lstrip('/').rstrip('/')
            # add path to the set
            disallowed_paths.add(university_url+path)
            print(f"line: {line}, path_parsed: {path}")

def scraper(university_url, robots_txt):

    # make a set to hold disallowed paths
    disallowed_paths = set()
    
    # parse the robots.txt file and add the disallowed paths to the disallowed_paths set
    parse_robots_txt(robots_txt, disallowed_paths, university_url)
    # print the disallowed paths
    print(f"Disallowed Paths: {disallowed_paths}")

    # TODO: add comments here
    loader = RecursiveUrlLoader(
        url=university_url, 
        max_depth=10, 
        exclude_dirs=disallowed_paths, 
        extractor=lambda x: Soup(x, "html.parser").text
    )

    # print what's in loader before loading
    print(f"loader_SCRAPER: {loader}")
    pages = loader.load()
    # print what's in pages after loading loader
    print(f"pages_SCRAPER: {pages}")
    
    # loop through each page, chope off the root url and then check if the
    # remaining URL extenstion is in disallowed paths
    for page_number, page in enumerate(pages):
        # Extract path after root URL (https://www.school.edu/)
        page_url = page.metadata['source']
        print(f"Path_SCRAPER = {[page_url]}")
        # if the path is not in the disallowed paths, then upload the page
        if page_url not in disallowed_paths:
            upload_page(page.page_content, page.metadata, page_number+1, university_url)

def sanitize_metadata(page_metadata):
    for key, value in page_metadata.items():
        if value is not None:
        # Replace newline characters with spaces
            sanitized_value = value.replace('\r\n', ' ')
            page_metadata[key] = sanitized_value
    return page_metadata

def upload_page(page_content, page_metadata, page_number, university_url):
    # i = current iteration, page = current page in pages
    print("starting upload on {page}, iteration: {i}")
    # getting the url associated with the page
    url = page_metadata['source']
    # rename the page to {university_name_(i+1)}, i.e. 'salisbury_university_page_1'
    blob_name = f"{university_url+url}_{page_number}"
    # upload the doc to the blob container
    try:
        sanitized_metadata = sanitize_metadata(page_metadata)
        if sum(len(k) + len(str(v)) for k, v in sanitized_metadata.items()) <= 8192:
            blob_tools.data_upload(blob_name, page_content, sanitized_metadata)
        else:
            print("Metadata size exceeds limit")
    except Exception as e:
        print(f"Error during upload: {e}")
    print(f"Done uploading Page: {page_number}")
    print("all pages uploaded")
    print(f"Following pages metadata was not uploaded, {blob_tools.oversized_metadata.keys()}")
    
university_info = { 
    "https://www.udel.edu/": "uofd_page",
    }
   #     "https://www.umbc.edu/": "umbc_page", 
    #"https://www.vt.edu/": "vt_page", 
    #"https://collegescorecard.ed.gov/": "collegescorecard_page",
    #"https://www.collegeconfidential.com/": "collegeconfidential_page",
    #"https://www.unigo.com/": "unigo_page",
university_urls = list(university_info.keys())
for university_url in university_urls:
    robots_txt_url = university_url + "robots.txt" 
    robots_txt = download_robots_txt(robots_txt_url)
    scraper(university_url, robots_txt)

