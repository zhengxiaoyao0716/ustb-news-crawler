#coding=UTF-8

from flask import Flask, request, jsonify
import data_util

app = Flask(__name__)


#####################Util#####################
##包装返回体
def pack_responce(success, content, message = None):
    return jsonify({'success': success, 'content': content, 'message': message})


#####################Api#####################
#抓取数据
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
        
        
import requests
from bs4 import BeautifulSoup
#适配界面
@app.route('/view/<path:href>')
def view(href):
    base = "http://oice.ustb.edu.cn/"
    r = requests.get(base + href)
    r.encoding='UTF-8'
    html = r.text
    soup = BeautifulSoup(html, "html.parser")
    nav = soup.select('.z-2')[0]
    nav_str = u'当前位置 >'
    for a in nav.select('a'):
        #a['href']
        nav_str += '> ' + a.text + ' '
    record = soup.select('.y-13')[0]
    if not record:
        return html
    return '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"/>
    <base href=''' + base + '''/>
    <title>UstbNews</title>
    <link href="http://ustbnews.zheng0716.com/static/css/view.css" rel="stylesheet"/>
</head>
<body>
    <div class="nav"><p>''' + nav_str + '''</p></div>
    ''' + unicode(record) + '''
</body>
'''
    
    
#####################Run#####################
if __name__ == '__main__':
    app.run(debug = True, port = 5100)