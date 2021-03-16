from dotenv import load_dotenv
from json_convert import write_json
import pymongo
import time
import argparse
import os
import ssl
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import logging
ssl._create_default_https_context = ssl._create_unverified_context

logging.basicConfig(filename="scraper.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()

load_dotenv()
db_pw = os.getenv("PW")

book_urls = set()
book_to_load = []
author_to_load = []
author_urls = set()
book_next = []
appened_book = []
appened_author = []


def connect_db():
    client = pymongo.MongoClient(
        "mongodb+srv://rni42:"+db_pw +
        "@cluster0.l9fca.mongodb.net/goodreaddb?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)
    return client


def get_web_info(url):
    """ get web info given url

    Args:
        url (string): web url

    Returns:
        web_info : parsed html data as bs4 object
    """
    web_info = None
    try:
        req = urlopen(url)
        web_html = req.read()
        req.close()
        web_info = soup(web_html, "html.parser")
    except ValueError:
        logger.warning("Unknown url({})".format(url))
    finally:
        return web_info


def get_similar_book(web_book):
    """ get similar book url

    Args:
        web_book (bs4 object): html info about the book

    Returns:
        list: a list of similar books
    """
    node = web_book.find('a', text='See similar books…')
    # print(node)
    if not node:
        return []
    similar_book_url = node['href']

    web_similar_book = get_web_info(similar_book_url)
    book_list_html = web_similar_book.find_all('span', {'itemprop': 'name'})
    book_list = []
    book_url = web_similar_book.find_all('a', {'itemprop': 'url'})
    for i, book_html in enumerate(book_list_html):
        # since the book link is after author link
        if i % 2 == 0:
            book_list.append(book_html.string)
            book_next.append(
                'https://www.goodreads.com' + book_url[i]['href'])
    return book_list


def get_isbn(web_book):
    """get ISBN"""
    isbn = ''
    check_isbn = web_book.find(
        'div', {'class': 'infoBoxRowTitle'}, text='ISBN')
    if check_isbn:
        isbn = ' '.join(check_isbn.find_next_sibling().text.strip().split())
    if isbn != '':
        return isbn.split()[0]
    return isbn


def get_similar_author(web_author):
    """ helper function for get similar author from current author

    Args:
        web_author (bs4 object): html data of the author page

    Returns:
        list : returns a similar author list
    """
    node = web_author.find('a', text='Similar authors')
    if not node:
        return []
    similar_author_url = 'https://www.goodreads.com' + node['href']
    web_similar_author = get_web_info(similar_author_url)
    author_list_html = web_similar_author.find_all(
        'span', {'itemprop': 'name'})
    similar_author_list = [a.string for a in author_list_html]
    return similar_author_list


def content_helper(info_table, web_info, book):
    """ a helper function get rating, rating_count and imag_url

    Args:
        info_table (list): list of info string
        web_info (bs4 object): html data of the web
        book (boolean): a boolean object to determine if it's a book or author
    """

    info_table['rating'] = web_info.find(
        'span', {'itemprop': 'ratingValue'}).text.strip()
    tag = 'span'
    if book:
        tag = 'meta'
    info_table['rating_count'] = web_info.find(
        tag, {'itemprop': 'ratingCount'})['content']
    info_table['review_count'] = web_info.find(
        tag, {'itemprop': 'reviewCount'})['content']
    info_table['image_url'] = web_info.find(
        'meta', {'property': 'og:image'})['content']


def scrap_author(author_name, author_url):
    """ a function to scrap author info

    Args:
        author_name (string): the name of the author
        author_url (string): the url of author page
    """
    if author_url in author_urls:
        return
    web_author = get_web_info(author_url)
    if not web_author:
        return
    logger.warning("getting author")
    single_author = {}
    single_author['name'] = author_name
    single_author['author_url'] = author_url
    single_author['author_id'] = ''.join(
        filter(str.isdigit, author_url))
    content_helper(single_author, web_author, False)
    single_author['related_authors'] = get_similar_author(web_author)
    single_author['author_books'] = [
        a.string for a in web_author.find_all('span', {'itemprop': 'name'})]
    author_to_load.append(single_author)
    appened_author.append(single_author)
    author_urls.add(author_url)


def scrap_book(book_url, num_author_need):
    """ the function for scarpping book

    Args:
        book_url (string): url for this book
        num_author_need(int): need number of author
    Returns:
        list: a list of string contains book info
    """
    if book_url in book_urls:
        return None
    web_book = get_web_info(book_url)
    if not web_book:
        return None
    book_holder = {}
    book_title_node = web_book.find('h1', {'id': 'bookTitle'})
    if not book_title_node:
        return None
    logger.warning("getting Books")
    book_holder['book_url'] = book_url
    book_holder['title'] = book_title_node.string.strip()
    book_holder['book_id'] = ''.join(
        filter(str.isdigit, book_url))
    book_holder['ISBN'] = get_isbn(web_book)
    book_holder['author_url'] = web_book.find(
        'a', {'class': 'authorName'})['href']
    book_holder['author'] = web_book.find(
        'span', {'itemprop': 'name'}).getText()
    content_helper(book_holder, web_book, True)
    book_holder['similar_books'] = get_similar_book(web_book)
    book_to_load.append(book_holder)
    appened_book.append(book_holder)
    book_urls.add(book_url)
    if len(author_urls) >= num_author_need:
        return book_holder
    scrap_author(book_holder['author'], book_holder['author_url'])
    return book_holder


def main(num_book, num_author, url):
    """ this is a main function with command line interface allow user choose starting page,
     # of authors and # of books they want to scrap
    """
    time1 = time.time()
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--num_book', type=int, default=num_book)
    # parser.add_argument('--num_author', type=int, default=num_author)
    # parser.add_argument(
    #     '--url', type=str, default=url)
    # parser.add_argument('--export_to_json', type=bool, default=True)
    # args = parser.parse_args()
    export_to_json = False
    # connect to db
    client = client = pymongo.MongoClient(
        "mongodb+srv://rni42:"+db_pw +
        "@cluster0.l9fca.mongodb.net/goodreaddb?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)
    mydb = client.goodreaddb
    author = mydb["author"]
    book = mydb["book"]

    book_next.append(url)
    while len(book_urls) < num_book or len(author_urls) < num_author:
        if len(book_next) == 0:
            logger.warning("Not hit required value")
            break
        to_scrape = book_next[0]
        scrap_book(to_scrape, num_author)
        if len(author_to_load) > 0:
            single_author = author_to_load[0]
            author.replace_one(single_author, single_author, upsert=True)
            author_to_load.remove(single_author)
        if len(book_to_load) > 0:
            single_book = book_to_load[0]
            book.replace_one(single_book, single_book, upsert=True)
            book_to_load.remove(single_book)
        book_next.remove(to_scrape)
    if export_to_json:
        write_json(appened_book, 'book_test_7.json')
        write_json(appened_author, 'author_test_7.json')
    client.close()
    time2 = time.time()
    print("finish in " + str(time2 - time1))
    # result = []
    # result.append(appened_author)
    # result.append(appened_book)
    # return result
    return appened_book, appened_author


if __name__ == "__main__":
    main()
