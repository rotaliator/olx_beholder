import sqlite3
from collections import namedtuple
import configparser
import requests
from bs4 import BeautifulSoup
from pyhiccup.core import html
from cache_local import cache_local
from send_email import send_email_two_part


config = configparser.ConfigParser()
config.read('olx_beholder.ini')
sender = config['Message']['sender']
receiver = config['Message']['receiver']
bcc = config['Message'].get('bcc', '')
subject= config['Message']['subject']


Offer = namedtuple("Offer", "title link city price")

offers_to_send = []

def init_db(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS offers
                    (title text, link text UNIQUE, city text, price text)''')


def insert_offer(conn, title, link, city, price):
    try:
        conn.execute("INSERT INTO offers VALUES (?, ?, ?, ?)",
                     (title, link, city, price))
        conn.commit()
        print("new OFFER!")
        offers_to_send.append(Offer(title, link, city, price))
    except sqlite3.IntegrityError:
        pass

def format_body_text(offers):
    body_text = "\n".join(f'* {o.city} {o.price} {o.title} {o.link}\n' for o in offers)
    return body_text

def format_body_html(offers):
    margin_right = {"style": "margin-right: 3px;"}
    data = [
        ['div',
         ['ul',
          [['li',
            ['i', margin_right, o.city], ['b', margin_right, o.price], ['a', {'href': o.link}, o.title]]
           for o in offers]]
        ]
    ]
    body_html = html(data)
    body_html = body_html.replace('dir="rtl"', 'dir="ltr"')
    return body_html


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
    with open("urls.txt") as f:
        urls = [url for url in f if url]

    with sqlite3.connect('olx_beholder.db') as conn:
        init_db(conn)
        for url in urls:
            results = get_results(url)
            process_results(conn, results)

    if offers_to_send:
        body_text = format_body_text(offers_to_send)
        body_html = format_body_html(offers_to_send)
        print(body_text, "\n", body_html)
        send_email_two_part(receiver, sender, subject, body_text, body_html, bcc)


if __name__ == '__main__':
    main()
