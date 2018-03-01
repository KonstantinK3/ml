from pymongo import MongoClient #работа с pymongo
import pymongo
from pprint import pprint
from flask import jsonify

def writeDB(quotesData):
    client = MongoClient("mongodb://user:zx655poiQ@ds123381.mlab.com:23381/appsy")
    db = client.appsy #коннект к database (содержит коллекшены->документы)
    quotes = db.quotes #выбор коллекшна quotes
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
        print(res, end='\n\n')
        result = quotes.insert_one(res) #вставка документа в коллекш
    deleted = quotes.delete_many({})



writeDB(    
[['Просто потому, что его просто не понимаю.',
  'Just because its simple doesnt mean it makes sense.'],
 ['Плохой дизайн кричит на вас. Хороший дизайн-это молчаливый продавец. ',
  'Bad design shouts at you. Good design is the silent seller. '],
 ['Продукт редизайн для кого-то-всегда сложное дело. Ты не знаешь, почему они '
  'принимали решения, которые они сделали. У вас нет данных, у них нет.',
  'Redesigning somebody else’s product is always a tricky business. You don’t '
  'know why they made the decisions they made. You don’t have the data they '
  'have.'],
 ['Хороший дизайн начинается с честности, задает каверзные вопросы, идет от '
  'сотрудничества и доверять своей интуиции.',
  'Good design begins with honesty, asks tough questions, comes from '
  'collaboration and from trusting your intuition.'],
 ['Инновации редко мешает Платформа. ',
  'Innovation is seldom hindered by platform.  ']]      
 )