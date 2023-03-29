from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
from functions import *
from transformer import *
import time
import threading

app = Flask(__name__)
api = Api(app)

accountss = {
    1:{'twitter-handle':'cathiedwood'},
    2:{'twitter-handle':'taylorlorenz'},
    3:{'twitter-handle':'ylecun'},
}

model = SentimentClassifier()


data_cathiedwood_owner = pd.read_pickle('datasets/cathiedwood_owner.pkl')
data_cathiedwood_replies = pd.read_pickle('datasets/cathiedwood_replies.pkl')
data_ylecun_owner = pd.read_pickle('datasets/ylecun_owner.pkl')
data_ylecun_replies = pd.read_pickle('datasets/ylecun_replies.pkl')
data_taylorlorenz_owner = pd.read_pickle('datasets/taylorlorenz_owner.pkl')
data_taylorlorenz_replies = pd.read_pickle('datasets/taylorlorenz_replies.pkl')


data = {
    'cathiedwood':{'replies':data_cathiedwood_replies,'owner':data_cathiedwood_owner},
    'taylorlorenz':{'replies':data_taylorlorenz_replies,'owner':data_taylorlorenz_owner},
    'ylecun':{'replies':data_ylecun_replies,'owner':data_ylecun_owner},
}


class  accounts (Resource):
    def get(self):
     return accountss

class  tweets (Resource):
    def get(self,pk):
     return pd.read_pickle('datasets/'+pk+'_owner.pkl').to_json(orient='index')

class  audience (Resource):
    def get(self,pk):
        return active_audience(data[pk]['replies'],5).to_json(orient='index')

class  sentiment (Resource):
    def get(self,pk): 
        temp = sentiment_sum(data[pk]['owner'], column = 'Username')
        return  pd.DataFrame({'Type':['thread level'], 'Polarity sentiment score':[Polarity_Score([[temp[i] for i in range(3)]])]}).to_json(orient='index')

api.add_resource(accounts, '/accounts')
api.add_resource(audience, '/audience/<pk>')
api.add_resource(tweets, '/tweets/<pk>')
api.add_resource(sentiment, '/sentiment/<pk>')


def function_API():
    if __name__ == '__main__':
        app.run(host = '0.0.0.0', port = 5000)
       


def function_updator (model):
    while True: 
        if (time.time() % (3600*6)) <0.001:

            data_cathiedwood_owner = pd.read_pickle('datasets/cathiedwood_owner.pkl')
            data_cathiedwood_replies = pd.read_pickle('datasets/cathiedwood_replies.pkl')
            data_ylecun_owner = pd.read_pickle('datasets/ylecun_owner.pkl')
            data_ylecun_replies = pd.read_pickle('datasets/ylecun_replies.pkl')
            data_taylorlorenz_owner = pd.read_pickle('datasets/taylorlorenz_owner.pkl')
            data_taylorlorenz_replies = pd.read_pickle('datasets/taylorlorenz_replies.pkl')
            
            data_replies1 = data_update(data_cathiedwood_replies, 'cathiedwood', model, scraping_type = 'replies')
            data_owner1 = data_update(data_cathiedwood_owner, 'cathiedwood', model, scraping_type = 'owner')
            data_replies2 = data_update(data_ylecun_replies, 'ylecun', model, scraping_type = 'replies')
            data_owner2 = data_update(data_ylecun_owner, 'ylecun', model, scraping_type = 'owner')
            data_replies3 = data_update(data_taylorlorenz_replies, 'taylorlorenz', model, scraping_type = 'replies')
            data_owner3 = data_update(data_taylorlorenz_owner, 'taylorlorenz', model, scraping_type = 'owner')
            
            data_replies1.to_pickle('datasets/cathiedwood_replies.pkl')
            data_owner1.to_pickle('datasets/cathiedwood_owner.pkl')
            data_replies2.to_pickle('datasets/ylecun_replies.pkl')
            data_owner2.to_pickle('datasets/ylecun_owner.pkl')
            data_replies3.to_pickle('datasets/taylorlorenz_replies.pkl')
            data_owner3.to_pickle('datasets/taylorlorenz_owner.pkl')


            
threading.Thread(target=function_API).start()
threading.Thread(target=function_updator(model)).start()


