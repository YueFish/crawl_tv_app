#coding:utf-8
from pymongo import MongoClient
import json

client = MongoClient('mongodb://127.0.0.1:27017/',
                    username = 'admin',
                    password = 'password',
                    authSource ='admin',
                    authMechanism = 'SCRAM-SHA-1'
    )
db = client.usermap
collection = db.app_info
fr = open('./data/app_info.csv','r')

for line in fr.readlines():
    doc  = json.loads(line)
    collection.insert_one(doc)
    # break
fr.close()
