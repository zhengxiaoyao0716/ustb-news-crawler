#coding=UTF-8

import time, requests
from bs4 import BeautifulSoup
class Data(object):
    #报警，比如源页面改版导致解析失败
    def alarm(msg):
        pass
        
    #解析展示消息的table
    @staticmethod
    def parse_table(table):
        result = []
        for tr in table.select('tr'):
            tds = tr.select('.y-9')
            if not tds:
                continue
            if len(tds) != 3:
                alarm(u'3个td描述一则记录的规律失效')
            record = {
                'href': tds[1].a['href'],
                'text': tds[1].text,
                'date': tds[2].text
            }
            result.append(record)
        return result
        
    last_time = 0
    cache_data = {}
    def __init__(self):
        #降频
        if time.time() - Data.last_time < 30:
            self.data = Data.cache_data
            return
        Data.last_time = time.time()
        print('aaa')
        
        html = requests.get('http://oice.ustb.edu.cn/xinwenzhongxin/').text
        soup = BeautifulSoup(html, "html.parser")
        info_tables = soup.select('.y-13')
        if not info_tables:
            alarm(u'.y-13的table展示信息')
        Data.cache_data = self.data = {
            'notice': Data.parse_table(info_tables[0]),
            'news': Data.parse_table(info_tables[1])
        }
        
    #公告通知
    def notice(self):
        return self.data['notify']
        
    #新闻速递
    def news(self):
        return self.data['news']