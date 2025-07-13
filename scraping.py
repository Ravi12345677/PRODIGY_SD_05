import requests
from bs4 import BeautifulSoup
import csv

# URL to scrape
BASE_URL = 'http://books.toscrape.com/catalogue/page-{}.html'

# Convert star-rating text to number
def rating_to_number(rating_text):
    ratings = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    return ratings.get(rating_text, 0)

# Open a CSV file to write the data
with open('books.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Price', 'Rating'])

    for page in range(1, 6):  # Scraping first 5 pages (adjust as needed)
        print(f"🔎 Scraping page {page}...")
        url = BASE_URL.format(page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get all book containers
        books = soup.select('article.product_pod')

        for book in books:
            title = book.h3.a['title']
            price = book.select_one('.price_color').text.strip()
            rating_class = book.select_one('p.star-rating')['class'][1]
            rating = rating_to_number(rating_class)

            writer.writerow([title, price, rating])

print("✅ Scraping completed. Data saved to 'books.csv'")