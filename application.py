#coding=UTF-8

from flask import Flask, jsonify
from data_util import Data

app = Flask(__name__)

@app.route('/data')
def get_data():
    return jsonify(Data().data)
    

if __name__ == '__main__':
    app.run(debug = True, port = 5100)