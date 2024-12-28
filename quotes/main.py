import requests
from bs4 import BeautifulSoup
from csv import writer
from time import sleep
from random import choice

# List to store scraped data
all_quotes = []

# Base URL
url = "https://www.goodreads.com/quotes"

# Pagination URL
change_url = "/page/1"

# Scraping loop
while change_url:
    # Concatenate URLs and make a request
    res = requests.get(f"{url}{change_url}", headers={"User-Agent": "Mozilla/5.0"})
    print(f"Now scraping {url}{change_url}")
    soup = BeautifulSoup(res.text, "html.parser")

    # Extracting all quote elements
    quotes = soup.find_all(class_="quote")

    for quote in quotes:
        try:
            all_quotes.append({
                "text": quote.find(class_="quoteText").get_text(strip=True).split("―")[0].strip(),
                "author": quote.find(class_="authorOrTitle").get_text(strip=True),
                "bio-link": quote.find("a")["href"]
            })
        except AttributeError:
            # Skip quote if required data is missing
            continue

    # Find the next button
    next_btn = soup.find(class_="next_page")
    change_url = next_btn["href"] if next_btn and "href" in next_btn.attrs else None
    sleep(2)

# Randomly select a quote
quote = choice(all_quotes)
remaining_guess = 4
print("Here's a quote: ")
print(quote["text"])

guess = ''
while guess.lower() != quote["author"].lower() and remaining_guess > 0:
    guess = input(f"Who said this quote? Guesses remaining: {remaining_guess}: ")
    
    if guess.lower() == quote["author"].lower():
        print("CONGRATULATIONS!!! YOU GOT IT RIGHT")
        break
    remaining_guess -= 1

    if remaining_guess == 3:
        # Fetch author details for a hint
        res = requests.get(f"{url}{quote['bio-link']}", headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(res.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text(strip=True)
        birth_place = soup.find(class_="author-born-location").get_text(strip=True)
        print(f"Here's a hint: The author was born on {birth_date} {birth_place}.")
    elif remaining_guess == 2:
        print(f"Here's a hint: The author's first name starts with: {quote['author'][0]}")
    elif remaining_guess == 1:
        last_initial = quote["author"].split(" ")[-1][0]
        print(f"Here's a hint: The author's last name starts with: {last_initial}")
    else:
        print(f"Sorry, you ran out of guesses. The answer was {quote['author']}.")
