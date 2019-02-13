import sqlite3
import smtplib
import requests
from bs4 import BeautifulSoup
from cache_local import cache_local


conn = sqlite3.connect('olx_beholder.db')

conn.execute('''CREATE TABLE IF NOT EXISTS offers
             (title text, link text UNIQUE, city text, price text)''')


urls = [
    "https://www.olx.pl/motoryzacja/samochody/honda/accord/?search%5Bfilter_float_price%3Afrom%5D=18000&search%5Bfilter_float_price%3Ato%5D=30000&search%5Bfilter_float_year%3Afrom%5D=2005&search%5Bfilter_enum_petrol%5D%5B0%5D=petrol&search%5Bfilter_enum_car_body%5D%5B0%5D=sedan&search%5Bfilter_enum_country_origin%5D%5B0%5D=pl",
]

def insert_offer(title, link, city, price):
    try:
        conn.execute("INSERT INTO offers VALUES (?, ?, ?, ?)",
                     (title, link, city, price))
        conn.commit()
        print("new OFFER!")
    except sqlite3.IntegrityError:
        pass

def process_results(content):
    soup = BeautifulSoup(content, 'html.parser')
    content = soup.find("div", "content")
    offers = content.find_all("div", "offer-wrapper")
    print(f"Found {len(offers)} offers")
    for offer in offers:
        link_title = offer.h3.a
        title = link_title.strong.get_text().strip()
        link = link_title['href']
        city = offer.i.parent.get_text().strip()
        price = offer.find("p", "price").get_text().strip()
        print(f"title: {title}\nlink: {link}")
        print(city, price)
        insert_offer(title, link, city, price)

@cache_local
def get_results(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.content
    raise LookupError



def main():
    for url in urls:
        results = get_results(url)
        process_results(results)


if __name__ == '__main__':
    main()
