#coding=UTF-8

from flask import Flask, request, jsonify
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
    flag = request.args.get('flag', None)
    if flag and flag == crawler.flag:
        return pack_responce(True, {'flag': flag}, 'Please use local-cache data.')
    if crawler:
        return pack_responce(True, {'flag': crawler.flag, 'data': crawler.data})
    else:
        return pack_responce(False, None, 'Unkown page.')
    
@app.route('/view/<path:href>')
def view(href):
    return pack_responce(True, href)
    
    
#####################Run#####################
if __name__ == '__main__':
    app.run(debug = True, port = 5100)