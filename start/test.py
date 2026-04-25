import requests
from bs4 import BeautifulSoup
URL ="http://quotes.toscrape.com/"
response = requests.get(URL)
soup = BeautifulSoup(response.text,"html.parser")
quote_blocks = soup.find_all("div",class_= "quote")
all_quotes = []
for block in quote_blocks:
    text = block.find("span",class_="text").text
    author = block.find("small",class_= "author").text
    tags = [tag.text for tag in block.find_all("a",class_="tag")]