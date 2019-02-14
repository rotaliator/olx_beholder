import sqlite3
import requests
from bs4 import BeautifulSoup
from cache_local import cache_local


def init_db(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS offers
                    (title text, link text UNIQUE, city text, price text)''')


def insert_offer(conn, title, link, city, price):
    try:
        conn.execute("INSERT INTO offers VALUES (?, ?, ?, ?)",
                     (title, link, city, price))
        conn.commit()
        print("new OFFER!")
    except sqlite3.IntegrityError:
        pass


def process_results(conn, content):
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
        insert_offer(conn, title, link, city, price)


@cache_local
def get_results(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.content
    raise LookupError


def main():
    urls = []
    with open("urls.txt") as f:
        for url in f:
            if url:
                urls.append(url)

    with sqlite3.connect('olx_beholder.db') as conn:
        init_db(conn)
        for url in urls:
            results = get_results(url)
            process_results(conn, results)


if __name__ == '__main__':
    main()
