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

def getQuoteByID(id):
    quotes = openBase()
    thatQuote = quotes.find_one({"myid": id})
    try:
        thatQuote["_id"] = ""
    except:
        thatQuote = {
        'myid':0,
        'ru': '',
        'en': ''}
    return(thatQuote)
#    res = []
#    for i in thatQuote:
#    #    print(i)
#        j = []
#        j.append(i['myid'])
#        j.append(i['ru'])
#        j.append(i['en'])
#        res.append(j)
#    res1={}
#    res1['res'] = res
#    return(res1)

#getQuoteByID(14)
    
print(getQuoteByID(33))
    
    #maxRes = quotes.find_one(sort=[("myid", pymongo.DESCENDING)])
