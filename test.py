from flask import Flask
from flask_restful import Resource, Api
import threading
import time

app = Flask(__name__)
api = Api(app)

accountss = {
    1:{'twitter-handle':'cathiedwood'},
    2:{'twitter-handle':'taylorlorenz'},
    3:{'twitter-handle':'ylecun'},
}

class  accounts (Resource):
    def get(self):
     return accountss

api.add_resource(accounts, '/accounts')


def function_API():
    if __name__ == '__main__':
        app.run(host = '0.0.0.0', port = 5000)

def f1 ():
    while True:
        if time.time()%10==0:
          print(1)
        

threading.Thread(target=function_API).start()
threading.Thread(target=f1()).start()


