#coding=UTF-8

from flask import Flask, jsonify
import data_util

app = Flask(__name__)


#####################Util#####################
##包装返回体
def pack_responce(success, content, message = None):
    return jsonify({'success': success, 'content': content, 'message': message})


#####################Api#####################
@app.route('/data/<page>')
def data(page):
    crawler = data_util.fetch(page)
    if crawler:
        return pack_responce(True, crawler.data)
    else:
        return pack_responce(False, None, 'Unkown page.')
    
@app.route('/view/<href>')
def view(href):
    return pack_responce(True, href)
    
    
#####################Run#####################
if __name__ == '__main__':
    app.run(debug = True, port = 5100)