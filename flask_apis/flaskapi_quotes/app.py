from flask import Flask, request, jsonify
app = Flask(__name__)
import os
import requests
import json
from pymongo import MongoClient #работа с pymongo
import pymongo

@app.route('/')
def index():
    return 'quotes will be here'

@app.route("/quotes", methods = ['GET', 'POST'])
def makeQuotes():
    if request.method == 'POST':
        #Получить кол-во цитат, занести их в базу и вернуть цитаты с переводом
        #запрос вида /quotes&number=10
        number = request.args.get('number')
        return newQuotes(number)
    elif request.method == 'GET':
        #Получить список цитат из базы
        return allQuotes()

#Make another app.route() decorator here that takes in an integer id in the 
@app.route("/quotes/<int:id>", methods = ['GET', 'DELETE'])
def processQuotes(id):
    if request.method == 'GET':
        #вернуть цитатцу по ID
        return getQuoteByID(id)
    elif request.method == 'DELETE':
        #удалить цитатцу
        return deleteQuoteByID(id) 

def openBase():
    client = MongoClient("mongodb://user:zx655poiQ@ds123381.mlab.com:23381/appsy")
    db = client.appsy #коннект к database (содержит коллекшены->документы)
    quotes = db.quotes #выбор коллекшна quotes
    return quotes   

def writeDB(quotesData):
    quotes = openBase()
    maxRes = quotes.find_one(sort=[("myid", pymongo.DESCENDING)])
    if maxRes == None:
        j = 1
    else:
        j = maxRes['myid'] + 1
    for i in quotesData:
        res = {}
        res['myid'] = j
        res['ru'] = i[0]
        res['en'] = i[1]
        j += 1
        result = quotes.insert_one(res) #вставка документа в коллекш

def newQuotes(number):
    quotesUrl = f'http://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]={number}'
    badStrings = ['&#8217;','<p>','</p>','\n','<em>','</em>']
    h = requests.get(quotesUrl)
    AllQuotesObjest = json.loads(h.text)
    quotesArray = []
    for i in AllQuotesObjest:
        singleQuote = i['content']
        for j in badStrings:
            singleQuote = singleQuote.replace(j, '')
        quotesArray.append(singleQuote)
    translatedQuotesArray = []
    for q in quotesArray:
        ruEnPair = []
        translateUrl = f'https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20170519T151400Z.eb180246b582df79.57d1ef7451eb2730886aad3dd64724abd5427edd&text={q}&lang=en-ru&format=plain'
        t = requests.get(translateUrl)
        t1 = json.loads(t.text)
        try:
            ruEnPair.append(t1['text'][0])
            ruEnPair.append(q)
            translatedQuotesArray.append(ruEnPair)
        except:
            continue
    res = translatedQuotesArray
    writeDB(translatedQuotesArray)
    res1 = {}
    res1['res'] = translatedQuotesArray
    return jsonify(res1)
  
def allQuotes():
    quotes = openBase()
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
    return jsonify(res1)
    
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
    return(jsonify(thatQuote))
	
def deleteQuoteByID(id):
    quotes = openBase()
    resQuote = quotes.find_one({"myid": id})
    if resQuote == None:
        return f"не существует цитаты {id}"
    else:
        resQuote = quotes.delete_one({"myid": id})
        return f"цитата {id} удалена"

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)