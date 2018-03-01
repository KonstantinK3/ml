from pymongo import MongoClient #работа с pymongo
import pymongo
from pprint import pprint
from flask import jsonify
import json

import hashlib
def hash_password(password):
    password = password.encode('utf-8')
    password_hash = hashlib.sha224(password).hexdigest()
    return password_hash

#def verify_password(password):
#    return pwd_context.verify(password, self.password_hash)

p = input("enter the password: ")
print(f"hash: {hash_password(p)}")
