import requests
from  bs4 import BeautifulSoup
from csv import writer
from time import sleep
from random import choice

# list to store scraped data
all_quotes = []

# this is the given url
url = "https://www.goodreads.com/quotes"

# this url is keeping changing 
change_url = "/page/1"

while url:

    # concatenating both urls and making request too
    res = requests.get(f"{url}{change_url}")
    print(f"Now scrapping {url}{change_url}")
    soup = BeautifulSoup(res.text,"html.parser")

    # extracting all elements
    quotes = soup.find_all(class_="quote")

    for quote in quotes:
        all_quotes.append({
            "text": quote.find(class_ ="text").get_text(),
            "author":quote.find(class_ ="author").get_text(),
            "bio-link":quote.find("a")["hredf"]

        })
        
