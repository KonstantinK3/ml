from pymongo import MongoClient #работа с pymongo
import pymongo
from pprint import pprint
from flask import jsonify
import json

def allQuotes():
    client = MongoClient("mongodb://user:zx655poiQ@ds123381.mlab.com:23381/appsy")
    db = client.appsy #коннект к database (содержит коллекшены->документы)
    quotes = db.quotes #выбор коллекшна quotes
    allQuotes = quotes.find(sort=[("myid", pymongo.ASCENDING)])
    res = []
    for i in allQuotes:
    #    print(i)
        j = []
        j.append(i['myid'])
        j.append(i['ru'])
        j.append(i['en'])
        res.append(j)
    res1={}
    res1['res'] = res
    return(res1)
    
print(allQuotes())
    
    #maxRes = quotes.find_one(sort=[("myid", pymongo.DESCENDING)])
#    if maxRes == None:
#        j = 1
#    else:
#        j = maxRes['myid'] + 1
#    for i in quotesData:
#        res = {}
#        res['myid'] = j
#        res['ru'] = i[0]
#        res['en'] = i[1]
#        j += 1
#        print(res, end='\n\n')
#        result = quotes.insert_one(res) #вставка документа в коллекш
#    deleted = quotes.delete_many({})