import requests
from bs4 import BeautifulSoup
from time import sleep
import csv

def scrape_goodreads_quotes():
    all_quotes = []
    base_url = "https://www.goodreads.com/quotes"
    page = 1

    while page <= 5:  # Scraping first 5 pages
        try:
            url = f"{base_url}?page={page}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            print(f"Now Scraping {url}")
            
            soup = BeautifulSoup(res.text, "html.parser")
            quote_containers = soup.find_all("div", class_="quoteDetails")

            for container in quote_containers:
                try:
                    # Extract quote text
                    quote_text_div = container.find("div", class_="quoteText")
                    if quote_text_div:
                        quote_parts = quote_text_div.get_text(strip=True).split('―', 1)
                        quote_text = quote_parts[0].strip().strip('"').strip('"')
                        
                        # Extract author
                        author_span = container.find("span", class_="authorOrTitle")
                        if author_span:
                            author = author_span.get_text(strip=True)
                            
                            # Extract likes count
                            likes_span = container.find("div", class_="right")
                            likes = likes_span.get_text(strip=True).split()[0] if likes_span else "0"
                            
                            # Extract tags if available
                            tags_div = container.find("div", class_="greyText smallText")
                            tags = tags_div.get_text(strip=True).replace("tags:", "").strip() if tags_div else ""
                            
                            all_quotes.append({
                                "quote": quote_text,
                                "author": author,
                                "likes": likes,
                                "tags": tags
                            })
                            
                except Exception as e:
                    print(f"Error processing quote: {e}")
                    continue
            
            print(f"Collected {len(all_quotes)} quotes so far...")
            page += 1
            sleep(2)  # Rate limiting
            
        except requests.RequestException as e:
            print(f"Error scraping page {page}: {e}")
            break
            
    return all_quotes

def save_to_csv(quotes, filename="goodreads_quotes.csv"):
    """Save the scraped quotes to a CSV file"""
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            # Define the CSV headers
            headers = ['quote', 'author', 'likes', 'tags']
            writer = csv.DictWriter(file, fieldnames=headers)
            
            # Write the headers and data
            writer.writeheader()
            writer.writerows(quotes)
            
        print(f"\nSuccessfully saved {len(quotes)} quotes to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    print("Starting Goodreads quote scraper...")
    quotes = scrape_goodreads_quotes()
    
    if quotes:
        save_to_csv(quotes)
        print("\nScraping completed!")
        print(f"Total quotes collected: {len(quotes)}")
    else:
        print("No quotes were collected.")

if __name__ == "__main__":
    main()