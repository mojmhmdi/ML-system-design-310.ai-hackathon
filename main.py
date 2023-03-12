from flask import Flask
from flask_restful import Resource, Api
import pandas as pd
from functions import *
from transformer import *
app = Flask(__name__)
api = Api(app)

accountss = {
    1:{'twitter-handle':'cathiedwood'},
    2:{'twitter-handle':'taylorlorenz'},
    3:{'twitter-handle':'ylecun'},
}

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
     return data[pk]['owner'].to_json(orient='index')

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

if __name__ == '__main__':
    app.run()
    
