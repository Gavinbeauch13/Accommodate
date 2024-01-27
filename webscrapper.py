from bs4 import BeautifulSoup as Soup
from langchain_community.document_loaders.recursive_url_loader import RecursiveUrlLoader

url = "https://www.salisbury.edu/"
loader = RecursiveUrlLoader(
    url=url, max_depth=4, extractor=lambda x: Soup(x, "html.parser").text
)
docs = loader.load()

# Write the contents to a text file
output_file_path = "output.txt"
with open(output_file_path, "w", encoding="utf-8") as file:
    for doc in docs:
        file.write(str(doc) + "\n")

print(f"Contents of 'docs' have been saved to {output_file_path}")
