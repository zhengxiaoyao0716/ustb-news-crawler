#coding=UTF-8

import abc, time, requests
from bs4 import BeautifulSoup
#数据基类
class BaseData(object):
    __metaclass__ = abc.ABCMeta
    #报警，比如源页面改版导致解析失败
    @staticmethod
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
                BaseData.alarm(u'3个td描述一则记录的规律失效')
            record = {
                'href': tds[1].a['href'],
                'text': tds[1].text,
                'date': tds[2].text
            }
            result.append(record)
        return result
        
    last_time = 0
    def __init__(self, url):
        #降频
        now_time = time.time()
        if now_time - self.__class__.last_time < 30:
            self.data = self.__class__.data
            return
        self.__class__.last_time = now_time
               
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        self.__class__.data = self.data = self.parse(soup)
        
    #解析
    @abc.abstractmethod
    def parse(self, soup):
        pass
        
        
#主界面
class HomeData(BaseData):
    def __init__(self):
        super(HomeData, self).__init__('http://oice.ustb.edu.cn/xinwenzhongxin/')
        
    def parse(self, soup):
        info_tables = soup.select('.y-13')
        if not info_tables:
            BaseData.alarm(u'.y-13的table展示信息')
        return {
            'notice': BaseData.parse_table(info_tables[0]),
            'news': BaseData.parse_table(info_tables[1])
        }
        
    #公告通知
    def notice(self):
        return self.data['notify']
        
    #新闻速递
    def news(self):
        return self.data['news']
        
        
#公告
class NoticeData(BaseData):
    def __init__(self):
        super(NoticeData, self).__init__('http://oice.ustb.edu.cn/xinwenzhongxin/gonggaotongzhi/')
        
    def parse(self, soup):
        info_tables = soup.select('.y-13')
        if not info_tables:
            BaseData.alarm(u'.y-13的table展示信息')
        return {'records': BaseData.parse_table(info_tables[0])}
        
        
#新闻
class NewsData(BaseData):
    def __init__(self):
        super(NewsData, self).__init__('http://oice.ustb.edu.cn/xinwenzhongxin/xinwensudi/')
        
    def parse(self, soup):
        info_tables = soup.select('.y-13')
        if not info_tables:
            BaseData.alarm(u'.y-13的table展示信息')
        return {'records': BaseData.parse_table(info_tables[0])}
        
        
#holder
dataMap = {
    'home': HomeData(),
    'notice': NoticeData(),
    'news': NewsData()
}
def fetch(page):
    if page in dataMap:
        return dataMap[page]
    else:
        return False