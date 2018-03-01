from pymongo import MongoClient #работа с pymongo
import pymongo
from pprint import pprint
from flask import jsonify
import json

def openBase():
    client = MongoClient("mongodb://user:zx655poiQ@ds123381.mlab.com:23381/appsy")
    db = client.appsy #коннект к database (содержит коллекшены->документы)
    quotes = db.quotes #выбор коллекшна quotes
    return quotes    

def deleteQuoteByID(id):
    quotes = openBase()
    resQuote = quotes.find_one({"myid": id})
    if resQuote == None:
        return f"не существует цитаты {id}"
    else:
        resQuote = quotes.delete_one({"myid": id})
        return f"цитата {id} удалена"
    
print(deleteQuoteByID(2))
    
    #maxRes = quotes.find_one(sort=[("myid", pymongo.DESCENDING)])
