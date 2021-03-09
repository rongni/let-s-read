""" api class"""
import json
from flask import Flask, request, render_template
from api_util import response_helper, parser_helper, get_request, post_helper
from api_util import post_scrape_helper, update_db_helper, delete_helper
import argparse
app = Flask(__name__)


@app.route("/")
def home():
    """ html default main page
    """
    return render_template("first.html")


@app.route("/search", methods=['GET'])
def search_query():
    """GET endpoint will handle search query get"""
    # query = request.args.get('q')
    if args.query is None:
        query = request.args['q']
    else:
        query = args.query.strip("'")
    # return (query)
    if ":" not in query:
        return response_helper("invalid query", 400)
    try:
        data = parser_helper(query)
        if data is None:
            return response_helper("cannot find book", 500)
        print(data)
        return data, 200
    except Exception:
        return response_helper("internal error", 500)


@app.route("/books", methods=['GET'])
def get_some_book():
    """GET endpoint.get book based on id """

    # id_value = request.args.get('book_id').strip('"')
    if args.book_id is None:
        id_value = request.args['book_id'].strip('"')
    else:
        id_value = args.book_id.strip('"')
    try:
        data = get_request(id_value, True, 'book_id')
        if data is None:
            return response_helper("cannot find book", 500)
        print(data)
        return data, 200
    except Exception:
        return response_helper("internal error", 500)


@app.route("/authors", methods=['GET'])
def get_some_author():
    """GET endpoint,get author base one id """
    # id_value = request.args.get('author_id').strip('"')
    if args.author_id is None:
        id_value = request.args['author_id'].strip('"')
    else:
        id_value = args.author_id.strip('"')
    try:
        data = get_request(id_value, False, 'author_id')
        if data is None:
            return response_helper("cannot find author", 500)
        print(data)
        return data, 200

    except Exception:
        return response_helper("internal error", 500)


@app.route("/authors", methods=['POST'])
def post_one_author_info():
    """
    POST endpoint
    post to database add author
    """
    # new_dict = json.loads(request.data)
    if args.infile is None:
        new_dict = json.loads(request.data)
    else:
        new_dict = json.load(args.infile[0])
    try:
        res = post_helper(False, new_dict)
        if res is None:
            return response_helper("cannot post author", 500)
        print("success")
        return response_helper(res, 200)
    except Exception:
        return response_helper("internal error", 500)


@app.route("/books", methods=['POST'])
def post_one_book_info():
    """POST endpoint,add book to database"""
    new_dict = json.loads(request.data)
    try:
        res = post_helper(True, new_dict)
        if res is None:
            return response_helper("cannot post book", 500)
        return response_helper(res, 200)
    except Exception:
        return response_helper("internal error", 500)


@app.route("/scrape", methods=['POST'])
def post_scrape():
    """
    POST endpoint
    user can scrape book and author base on input url
    """
    if args.urlm is None:
        url = request.args.get('attr').strip('"')
    else:
        url = args.urlm.strip('"')
    try:
        res = post_scrape_helper(url)
        if res is None:
            return response_helper("cannot post book/author", 500)
        return res
    except Exception:
        return response_helper("internal error", 500)


@app.route("/books", methods=['PUT'])
def put_book_info():
    """
    PUT endpoint
    /book?book_id=The Lakehouse&ISBN=1234
    """
    if args.json_list is None:
        new_dict = json.loads(request.data)
    else:
        new_dict = json.loads(args.json_list)
    if args.book_id is None:
        id_value = request.args['book_id'].strip('"')
    else:
        id_value = args.book_id.strip('"')
    try:
        book_doc = get_request(id_value, True, 'book_id')
        if book_doc is None:
            return response_helper("cannot find book", 500)
        res = update_db_helper(book_doc, new_dict, True)
        if res is None:
            return response_helper("update failed", 500)
        print("success")
        return "success updated"
    except Exception:
        return response_helper("internal error", 500)


@app.route("/authors", methods=['PUT'])
def put_author_info():
    """
    PUT endpoint
    /authors?author_id=1234&ISBN=1234
    """
    if args.json_list is None:
        new_dict = json.loads(request.data)
    else:
        new_dict = json.loads(args.json_list)
    if args.book_id is None:
        id_value = request.args['author_id'].strip('"')
    else:
        id_value = args.author_id.strip('"')
    try:
        author_doc = get_request(id_value, False, 'author_id')
        if author_doc is None:
            return response_helper("cannot find author", 500)
        res = update_db_helper(author_doc, new_dict, False)
        if res is None:
            return response_helper("update failed", 500)
        print("success updated")
        return "success updated"
    except Exception:
        return response_helper("internal error", 500)


@app.route("/books", methods=['DELETE'])
def delete_book():
    """DELETE endpoint,delte a book base on id """
    if args.book_id is None:
        id_value = request.args.get('book_id').strip('"')
    else:
        id_value = args.book_id.strip('"')
    try:
        to_delete = get_request(id_value, True, 'book_id')
        if to_delete is None:
            return response_helper("cannot find book", 500)
        check = delete_helper(to_delete, True)
        if check:
            print("success")
            return response_helper("deleted success", 200)
        return response_helper("cannot find book to delete", 400)
    except Exception:
        return response_helper("internal error", 500)


@app.route("/authors", methods=['DELETE'])
def delete_author():
    """
    GET endpoint
    /authors?attr={attr_value} Example: /authors?author_title=Joe Clifford
    :return: json object of author filtered
    """
    # id_value = request.args.get('author_id').strip('"')
    if args.author_id is None:
        id_value = request.args.get('author_id').strip('"')
    else:
        id_value = args.author_id.strip('"')
    try:
        to_delete = get_request(id_value, False, 'author_id')
        if to_delete is None:
            return response_helper("cannot find author", 500)
        check = delete_helper(to_delete, False)
        if check:
            print("success")
            return response_helper("deleted success", 200)
        return response_helper("cannot find author to delete", 400)
    except Exception:
        return response_helper("internal error", 500)


parser = argparse.ArgumentParser(description='API server')
parser.add_argument('-bi', '--book_id', type=str,
                    help='book_id for get, put and delete book information')
parser.add_argument('-ai', '--author_id', type=str,
                    help='author_id for get, put and delete author information')
parser.add_argument('-query', '--query', type=str,
                    help='query for get author or book infromation')
parser.add_argument('-json_list', '--json_list', type=str,
                    help='json_list for update book or author information')
parser.add_argument('-urlm', '--urlm', type=str,
                    help='The url start to scrape')
parser.add_argument('-f', '--infile', nargs=1,
                    help="JSON file to be processed",
                    type=argparse.FileType('r'))
# parser.add_argument('-na', '--numberofauthors', type=int,
#                     help='Number of authors user want to input', default5)
# parser.add_argument('-nb', '--numberofbooks', type=int,
#                     help='Number of books user want to input', default=10)

group = parser.add_mutually_exclusive_group()
group.add_argument('-gb', '--getbook', action='store_true',
                   help='get book information')
group.add_argument('-ga', '--getauthor', action='store_true',
                   help='get author information')
group.add_argument('-putb', '--putbook', action='store_true',
                   help='update book information')
group.add_argument('-puta', '--putauthor', action='store_true',
                   help='update author information')
group.add_argument('-postb', '--postbook', action='store_true',
                   help='add new book information')
group.add_argument('-posta', '--postauthor',
                   action='store_true', help='add new author information')
group.add_argument('-db', '--deletebook', action='store_true',
                   help='delete book information')
group.add_argument('-da', '--deleteauthor', action='store_true',
                   help='delete author information')
group.add_argument('-search', '--search', action='store_true',
                   help='search information by query')
group.add_argument('-sb', '--scrapebook_author', action='store_true',
                   help='scrape book information')
args = parser.parse_args()

if __name__ == '__main__':
    if args.getbook:
        get_some_book()
    elif args.getauthor:
        get_some_author()
    elif args.putbook:
        put_book_info()
    elif args.putauthor:
        put_author_info()
    elif args.postbook:
        post_one_book_info()
    elif args.postauthor:
        post_one_author_info()
    elif args.deletebook:
        delete_book()
    elif args.deleteauthor:
        delete_author()
    elif args.search:
        search_query()
    elif args.scrapebook_author:
        post_scrape()
    else:
        app.run(debug=True)
