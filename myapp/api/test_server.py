import server
import unittest
from flask_testing import TestCase

BASE = "http://127.0.0.1:5000/"


class MyTest(TestCase):
    def create_app(self):
        server.app.config['TESTING'] = True
        return server.app

    def test_search_id(self):
        response = self.client.get('search?q=author.author_id:153394')
        self.assertEqual(response.status_code, 200)

    def test_search_easy(self):
        response = self.client.get('search?q=author.name:Suzanne Collins')
        self.assertEqual(response.status_code, 200)

    def test_search_quotation(self):
        response = self.client.get('search?q=book.book_id:"438456053"')
        self.assertEqual(response.status_code, 200)

    def test_search_or(self):
        response = self.client.get(
            'search?q=book.book_id:438456053OR44428156')
        self.assertEqual(response.status_code, 200)

    def test_search_and(self):
        response = self.client.get(
            'search?q=book.book_id:438456053ANDISBN:1506708137')
        self.assertEqual(response.status_code, 200)

    def test_search_not(self):
        response = self.client.get('search?q=book.book_id:NOT438456053')
        self.assertEqual(response.status_code, 200)

    def test_search_greater(self):
        response = self.client.get('search?q=book.review_count:>1000')
        self.assertEqual(response.status_code, 200)

    def test_search_less(self):
        response = self.client.get('search?q=book.review_count:<100')
        self.assertEqual(response.status_code, 200)

    def test_getbook(self):
        response = self.client.get('books?book_id=18144590')
        self.assertEqual(response.status_code, 200)

    def test_getauthor(self):
        response = self.client.get('authors?author_id=153394')
        self.assertEqual(response.status_code, 200)

    def test_postbook(self):
        response = self.client.post('books', json=[{"book_url": "https://www.goodreads.com/book/show/43845605-imbalance-part-2", "title": "Imbalance, Part 3", "book_id": "438456053", "ISBN": "1506708137",
                                                    "author_url": "https://www.goodreads.com/author/show/996558.Faith_Erin_Hicks", "author": "Faith Erin Hicks", "rating": "4.31", "rating_count": "1742",
                                                    "review_count": "105", "image_url": "https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1549389961i/43845605._UY630_SR1200,630_.jpg",
                                                    "similar_books": ["Imbalance, Part 3 (Avatar: The Last Airbender: Imbalance, #3)", "Avatar: The Last Airbender: North and South, Part 3 (North and South, #3)",
                                                                      "Avatar: The Last Airbender: North and South, Part 2 (North and South, #2)", "Avatar: The Last Airbender: North and South, Part 1 (North and South, #1)",
                                                                      "Avatar: The Last Airbender- Smoke and Shadow, Part 3 (Smoke and Shadow, #3)", "Avatar: The Last Airbender - Smoke and Shadow, Part 2 (Smoke and Shadow, #2)",
                                                                      "Avatar: The Last Airbender - Smoke and Shadow, Part 1 (Smoke and Shadow, #1)", "Avatar: The Last Airbender: The Rift, Part 3 (The Rift, #3)", "Avatar: The Last Airbender - The Rift, Part 2 (The Rift, #2)", "Avatar: The Last Airbender - The Rift, Part 1 (The Rift, #1)", "Avatar: The Last Airbender: Team Avatar Tales (Avatar: The Last Airbender)",
                                                                      "Avatar: The Last Airbender - The Search, Part 3 (The Search, #3)", "Avatar: The Last Airbender - The Search, Part 2 (The Search, #2)", "Avatar: The Last Airbender - The Promise, Part 3 (The Promise, #3)", "Avatar: The Last Airbender - The Search, Part 1 (The Search, #1)", "The Legend of Korra: Ruins of the Empire, Part Two (Ruins of the Empire, #2)", "The Legend of Korra: Ruins of the Empire, Part Three (Ruins of the Empire, #3)", "Avatar: The Last Airbender - The Promise, Part 2 (The Promise, #2)", "Avatar: The Last Airbender: The Lost Adventures (Avatar: The Last Airbender)", "The Legend of Korra: Ruins of the Empire, Part One (Ruins of the Empire, #1)", "The Legend of Korra: Turf Wars, Part Two (The Legend of Korra: Turf Wars #2)", "The Legend of Korra: Turf Wars, Part Three (The Legend of Korra: Turf Wars, #3)", "The Legend of Korra: Turf Wars, Part One (The Legend of Korra: Turf Wars #1)", "Avatar: The Last Airbender - The Promise, Part 1 (The Promise, #1)", "FCBD 2013", "The Legend of Korra: Lost Pets (Free Comic Book Day 2018)", "FCBD 2015 #6", "The Lost Adventures and Team Avatar Tales (Avatar: The Last Airbender)", "Avatar: The Last Airbender: Legacy of The Fire Nation", "The Last Airbender: Prequel - Zuko's Story", "Avatar: The Last Airbender - Relics (Free Comic Book Day 2011)"]}])
        self.assertEqual(response.status_code, 200)

    def test_putbook(self):
        response = self.client.put('books?book_id="438456053"', json={
                                   "book_url": "https://www.goodreads.com/book/show/43845605-imbalance-part-3"})
        self.assertEqual(response.status_code, 200)

    def test_postauthor(self):
        response = self.client.post('authors', json=[{"name": "Carl Sagan", "author_url": "https://www.goodreads.com/author/show/10538.Carl_Sagan_text", "author_id": "10538", "rating": "4.23", "rating_count": "428230", "review_count": "14208", "image_url": "https://images.gr-assets.com/authors/1475953320p8/10538.jpg", "related_authors": ["Carl Sagan", "Bill Bryson", "Brian Greene", "Richard Dawkins", "Stephen Hawking", "David Filkin", "Kip S. Thorne", "John Gribbin", "Matt Ridley", "Simon Singh", "Charles Darwin", "Neil deGrasse Tyson", "Michio Kaku", "Steven Weinberg", "Jerry A. Coyne", "Richard P. Feynman", "Daniel C. Dennett"], "author_books": [
                                    "Carl Sagan", "Cosmos", "Contact", "Carl Sagan", "William Olivier Desmond", "The Demon-Haunted World: Science as a Candle in the Dark", "Pale Blue Dot: A Vision of the Human Future in Space", "Carl Sagan", "Ann Druyan", "Dragons of Eden: Speculations on the Evolution of Human Intelligence", "Billions & Billions: Thoughts on Life and Death at the Brink of the Millennium", "Carl Sagan", "Ann Druyan", "Broca's Brain: Reflections on the Romance of Science", "The Varieties of Scientific Experience: A Personal View of the Search for God", "Carl Sagan", "Ann Druyan", "Shadows of Forgotten Ancestors", "Carl Sagan", "Ann Druyan", "Cosmic Connection: An Extraterrestrial Perspective", "Carl Sagan", "Jerome Agel", "Ann Druyan"]}])
        self.assertEqual(response.status_code, 200)

    def test_putauthor(self):
        response = self.client.put('authors?author_id="10538"', json={
                                   "author_url": "https://www.goodreads.com/author/show/10538.Carl_Sagan"})
        self.assertEqual(response.status_code, 200)

    def test_scrapebook_author(self):
        response = self.client.post(
            '/scrape?attr="https://www.goodreads.com/book/show/38346154-beastars-2"')
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        response = self.client.delete('books?book_id=1617')
        self.assertEqual(response.status_code, 200)

    def test_delete_book_fail(self):
        response = self.client.delete('books?book_id=1617')
        self.assertEqual(response.status_code, 500)

    def test_delete_author(self):
        response = self.client.delete('authors?author_id=2383')
        self.assertEqual(response.status_code, 200)

    def test_delete_author_fail(self):
        response = self.client.delete('authors?author_id=2383')
        self.assertEqual(response.status_code, 500)


if __name__ == '__main__':
    unittest.main()
