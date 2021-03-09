import server
import unittest
from flask_testing import TestCase

BASE = "http://127.0.0.1:5000/"


class MyTest(TestCase):
    def create_app(self):
        server.app.config['TESTING'] = True
        return server.app

    def test_search_id(self):
        response = self.client.get('search?q=author.author_id:1265')
        self.assertEqual(response.status_code, 200)

    def test_search_easy(self):
        response = self.client.get('search?q=author.name:Jane Austen')
        self.assertEqual(response.status_code, 200)

    def test_search_quotation(self):
        response = self.client.get('search?q=book.book_id:"438456053"')
        self.assertEqual(response.status_code, 200)

    def test_search_or(self):
        response = self.client.get(
            'search?q=book.book_id:"438456053"OR"44428156"')
        self.assertEqual(response.status_code, 200)

    def test_search_and(self):
        response = self.client.get(
            'search?q=book.book_id:"438456053"ANDISBN:"1506708137"')
        self.assertEqual(response.status_code, 200)

    def test_search_not(self):
        response = self.client.get('search?q=book.book_id:NOT"438456053"')
        self.assertEqual(response.status_code, 200)

    def test_search_greater(self):
        response = self.client.get('search?q=book.review_count:>1000')
        self.assertEqual(response.status_code, 200)

    def test_search_less(self):
        response = self.client.get('search?q=book.review_count:<100')
        self.assertEqual(response.status_code, 200)

    def test_getbook(self):
        response = self.client.get('books?book_id=438456053')
        self.assertEqual(response.status_code, 200)

    def test_getauthor(self):
        response = self.client.get('authors?author_id=153394')
        self.assertEqual(response.status_code, 200)

    def test_putbook(self):
        response = self.client.put('books?book_id="77203"', json={
                                   "image_url": "https://s.gr-assets.com/assets/nophoto/user/f_700x9334-5899cba5f75bf635..."})
        self.assertEqual(response.status_code, 200)

    def test_putauthor(self):
        response = self.client.put('authors?author_id="153394"', json={
                                   "author_url": "https://www.goodreads.com/author/show/1533944.Suzanne_Collins"})
        self.assertEqual(response.status_code, 200)

    def test_postbook(self):
        response = self.client.post('books', json=[{"book_url": "https://www.goodreads.com/book/show/38346154-beastars-2", "title": "BEASTARS 2", "book_id": "383461542", "ISBN": "4253227554", "author": "Paru Itagaki, ", "author_url": "https://www.goodreads.com/author/show/17678083.Paru_Itagaki", "rating": {"numberDouble": "4.32"}, "rating_count": {"numberInt": "2237"}, "review_count": {"numberInt": "166"}, "image_url": "/book/photo/38346154-beastars-2", "similar_books": ["https://www.goodreads.com/book/show/52950513-spy-family-2", "https://www.goodreads.com/book/show/40553160-1", "https://www.goodreads.com/book/show/41583802-2", "https://www.goodreads.com/book/show/48729531-spy-family-3", "https://www.goodreads.com/book/show/44001132-4", "https://www.goodreads.com/book/show/43619964-3", "https://www.goodreads.com/book/show/45731760-kaiju-girl-caramelise-vol-2", "https://www.goodreads.com/book/show/52961491-spy-family-1", "https://www.goodreads.com/book/show/52373478-17-kimetsu-no-yaiba-17", "https://www.goodreads.com/book/show/42075170-1-jujutsu-kaisen-1",
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            "https://www.goodreads.com/book/show/25565269-18-akatsuki-no-yona-18", "https://www.goodreads.com/book/show/36646057-6-dungeon-meshi-6", "https://www.goodreads.com/book/show/36058455-17-boku-no-hero-academia-17", "https://www.goodreads.com/book/show/43160733-2-jujutsu-kaisen-2", "https://www.goodreads.com/book/show/43909475-komi-can-t-communicate-vol-3", "https://www.goodreads.com/book/show/38340632-7", "https://www.goodreads.com/book/show/32919053-golden-kamuy-vol-2", "https://www.goodreads.com/book/show/30751398-4", "https://www.goodreads.com/book/show/42858205-beastars-vol-1", "https://www.goodreads.com/book/show/38346754-beastars-3", "https://www.goodreads.com/book/show/38460931-beastars-4", "https://www.goodreads.com/book/show/39861173-beastars-5", "https://www.goodreads.com/book/show/39902449-beastars-6", "https://www.goodreads.com/book/show/39902338-beastars-7", "https://www.goodreads.com/book/show/41018558-beastars-8", "https://www.goodreads.com/book/show/42508426-beastars-9", "https://www.goodreads.com/book/show/42508435-beastars-10", "https://www.goodreads.com/book/show/42508660-beastars-11"]}])
        self.assertEqual(response.status_code, 200)

    def test_postauthor(self):
        response = self.client.post('authors', json=[{"name": "Carl Sagan", "author_url": "https://www.goodreads.com/author/show/10538.Carl_Sagan", "author_id": "10538", "rating": "4.23", "rating_count": "428230", "review_count": "14208", "image_url": "https://images.gr-assets.com/authors/1475953320p8/10538.jpg", "related_authors": ["Carl Sagan", "Bill Bryson", "Brian Greene", "Richard Dawkins", "Stephen Hawking", "David Filkin", "Kip S. Thorne", "John Gribbin", "Matt Ridley", "Simon Singh", "Charles Darwin", "Neil deGrasse Tyson", "Michio Kaku", "Steven Weinberg", "Jerry A. Coyne", "Richard P. Feynman", "Daniel C. Dennett"], "author_books": [
                                    "Carl Sagan", "Cosmos", "Contact", "Carl Sagan", "William Olivier Desmond", "The Demon-Haunted World: Science as a Candle in the Dark", "Pale Blue Dot: A Vision of the Human Future in Space", "Carl Sagan", "Ann Druyan", "Dragons of Eden: Speculations on the Evolution of Human Intelligence", "Billions & Billions: Thoughts on Life and Death at the Brink of the Millennium", "Carl Sagan", "Ann Druyan", "Broca's Brain: Reflections on the Romance of Science", "The Varieties of Scientific Experience: A Personal View of the Search for God", "Carl Sagan", "Ann Druyan", "Shadows of Forgotten Ancestors", "Carl Sagan", "Ann Druyan", "Cosmic Connection: An Extraterrestrial Perspective", "Carl Sagan", "Jerome Agel", "Ann Druyan"]}])
        self.assertEqual(response.status_code, 200)

    def test_scrapebook_author(self):
        response = self.client.post(
            '/scrape?attr="https://www.goodreads.com/book/show/38346154-beastars-2"')
        self.assertEqual(response.status_code, 200)

    def test_delete_book(self):
        response = self.client.delete('books?book_id=48855')
        self.assertEqual(response.status_code, 200)

    def test_delete_book_fail(self):
        response = self.client.delete('books?book_id=18135')
        self.assertEqual(response.status_code, 500)

    def test_delete_author(self):
        response = self.client.delete('authors?author_id="10538"')
        self.assertEqual(response.status_code, 200)

    def test_delete_author_fail(self):
        response = self.client.delete('authors?author_id="10538"')
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
