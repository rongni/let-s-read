"""all helper function for api"""
import json
import re
import os
import ssl
from flask import Response
import pymongo
# import myapp.api.scraper
from scraper import main
import dotenv
from dotenv import load_dotenv

load_dotenv()
db_pw = os.getenv("PW")


def connect_db():
    client = pymongo.MongoClient(
        "mongodb+srv://rni42:"+db_pw +
        "@cluster0.l9fca.mongodb.net/goodreaddb?retryWrites=true&w=majority",
        ssl_cert_reqs=ssl.CERT_NONE)
    return client


def get_request(id_val, is_book, field):
    """id request helper
    """
    my_client = connect_db()
    mydb = my_client.goodreaddb
    author = mydb["author"]
    book = mydb["book"]
    if is_book:
        books = book.find_one({field: id_val}, {'_id': 0})
        my_client.close()
        return books
    authors = author.find_one({field: id_val}, {'_id': 0})
    my_client.close()
    return authors


def get_all_request(is_book, is_rating, limit_value):
    """id request helper
    """
    data = {}
    vis = []
    my_client = connect_db()
    mydb = my_client.goodreaddb
    author = mydb["author"]
    book = mydb["book"]
    if is_book:
        cur = book.find().limit(limit_value)
        for doc in cur:
            if is_rating:
                data[doc['title']] = doc['rating']
            else:
                data[doc['book_id']] = doc['title']
        my_client.close()
        return data
    cur = author.find().limit(limit_value)
    for doc in cur:
        if is_rating:
            data[doc['name']] = doc['rating']
            # vis.append({doc['name']:doc['rating']})
        else:
            data[doc['author_id']] = doc['name']
    # print(data)
    my_client.close()
    return data


def post_helper(is_book, data):
    """id post helper
    """
    my_client = connect_db()
    mydb = my_client.goodreaddb
    author = mydb["author"]
    book = mydb["book"]
    if is_book:
        res = book.insert_many(data)
        if res:
            my_client.close()
            return "success"
    res = author.insert_many(data)
    if res:
        my_client.close()
        return "success"
    my_client.close()
    return None


def post_scrape_helper(url):
    """
    get scrape helper
    """
    book, author = main(1, 1, url)
    dic = {}
    dic["book"] = book
    dic["author"] = author
    return "success"


def response_helper(msg, code):
    """ send response to user
    """
    return Response(
        response=json.dumps({"message": msg}),
        status=code,
        mimetype="application/json"
    )


def update_db_helper(need_updated, data, is_book):
    """ handle put in database
    """
    my_client = connect_db()
    mydb = my_client.goodreaddb
    author = mydb["author"]
    book = mydb["book"]
    if is_book:
        new_value = {"$set": data}
        books = book.update_one(need_updated, new_value, upsert=False)
        my_client.close()
        return books
    new_value = {"$set": data}
    authors = author.update_one(need_updated, new_value, upsert=False)
    my_client.close()
    return authors


def delete_helper(to_delete, is_book):
    """handle delete helper
    """

    my_client = connect_db()
    mydb = my_client.goodreaddb
    author = mydb["author"]
    book = mydb["book"]
    if is_book:
        res = book.delete_one(to_delete)
        my_client.close()
        return res
    res = author.delete_one(to_delete)
    my_client.close()
    return res


def parser_helper(query):
    """parse a query will support different operators
    """

    logical_operator = ['OR', 'NOT', 'AND']
    one_side_comparion = ['>', '<']

    # reg = ".*?"
    if 'AND' in query:
        q1, q2 = query.split("AND")
        key, valu1 = q1.split(":")
        field, atr1 = key.split('.')
        atr2, valu2 = q2.split(':')
        return operand_helper(field, atr1, valu1, atr2, valu2, "$and")
    field = query.split(":")[0]
    value = query.split(":")[1]
    p = re.compile(r'".*?"')
    if "." in field:
        col = field.split(".")[0]
        attr = field.split(".")[1]
    if '"' in value:
        result = p.search(value).group()
        if len(result) != len(value):
            return response_helper("invaild query", 400)
        check = [ele for ele in logical_operator if(ele in result)]
        check = check or [ele for ele in one_side_comparion if(ele in result)]
        if check:
            return response_helper("invaild query", 400)
        value = result.strip('"')
        data = simiple_parse(col, attr, value)
        return data
    if [ele for ele in logical_operator if(ele in value)]:
        if "OR" in value:
            value1, value2 = value.split('OR')
            value1 = value1.strip('"')
            value2 = value2.strip('"')
            return operand_helper(col, attr, value1, attr, value2, "$or")
        if "NOT" in value:
            var1 = value.strip('NOT')
            return operand_helper(col, attr, var1, attr, var1, "$not")

    if [ele for ele in one_side_comparion if(ele in value)]:
        if ">" in value:
            value1, value2 = value.split(">")
            value2 = int(value2)
            print(attr)
            return operand_helper(col, attr, value2, attr, value2, "$gt")
        if "<" in value:
            value1, value2 = value.split("<")
            value2 = int(value2)
            # return (value1)
            return operand_helper(col, attr, value2, attr, value2, "$lt")
    return operand_helper(col, attr, value, attr, value, "contain")


def operand_helper(field, atr1, valu1, atr2, valu2, opt):
    """ helper for parse
    """

    my_client = connect_db()
    mydb = my_client.goodreaddb
    author = mydb["author"]
    book = mydb["book"]
    if field == 'book':
        if opt == "contain":
            cur = book.find({atr1: {'$regex': '.*' + valu1 + '.*'}})
            my_client.close()
            return cursor_helper(cur, True)
        if opt == "$gt" or opt == "$lt":
            cur = book.find({atr1: {opt: valu1}})
            my_client.close()
            return cursor_helper(cur, True)
        if opt == "$not":
            cur = book.find({atr1: {"$not": {'$regex': valu1}}})
            return cursor_helper(cur, True)
        cur = book.find(
            {opt: [{atr1: {'$regex': valu1}}, {atr2: {'$regex': valu2}}]})
        my_client.close()
        return cursor_helper(cur, True)
    if opt == "contain":
        cur = author.find({atr1: {'$regex': '.*' + valu1 + '.*'}})
        my_client.close()
        return cursor_helper(cur, False)
    if opt == "$gt" or opt == "$lt":
        cur = author.find({atr1: {opt: valu1}})
        my_client.close()
        return cursor_helper(cur, False)
    if opt == "$not":
        cur = author.find({atr1: {"$not": {'$regex': valu1}}})
        return cursor_helper(cur, False)
    cur = author.find(
        {opt: [{atr1: {'$regex': valu1}}, {atr2: {'$regex': valu2}}]})
    my_client.close()
    return cursor_helper(cur, False)


def cursor_helper(cur, isBook):
    """iterate through the cursor to get data 
    """
    res = []
    data = dict()
    count = 0
    if isBook:
        if cur is None:
            return None
        for doc in cur:
            if count > 20:
                break
            res.append(doc["title"])
            count = count+1
        data["book_title"] = res
        return data
    if cur is None:
        return None
    for doc in cur:
        if count > 20:
            break
        res.append(doc["name"])
        count = count+1
    data["author_name"] = res
    return data


def simiple_parse(col, attr, value):
    """ helper function when the user need exact match 
    """
    if col == 'book':
        book = get_request(value, True, attr)
        return book
    author = get_request(value, False, attr)
    return author
