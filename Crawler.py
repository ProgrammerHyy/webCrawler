import requests
import re
import random
from bs4 import BeautifulSoup

class Crawler:
    __url = ""

    # 类初始化
    def __init__(self, url):
        self.__url = url

    # 设置url
    def seturl(self, url):
        self.__url = url

    # 爬取数据
    def crawler(self):
        try:
            req = requests.get(self.__url, timeout=None)
            strhtml = req.text
            bf = BeautifulSoup(strhtml, features="html.parser")
            if bf.title.contents[0] == '404':
                return None
            return bf
        except Exception as  e:
            print('Unable to crawl info')
            return -1

    # 从网页中获取数据并写入数据库
    def getData(self, html):
        cnt = 0
        game = {}
        str = ""
        # 获取游戏标签
        try:
            taghtml = html.find(id='appTag')
            for child in taghtml.descendants:
                cnt += 1
                if cnt == 5:
                    str += child
                elif cnt == 6:
                    cnt = 0
            # 从字符串中拆分出tag并返回list
            tagList = re.split('\s+', str)
            del tagList[0]
            del tagList[len(tagList)-1]
            game['tag'] = tagList
            # 获取其他需要的参数并返回
            score = html.find(class_='app-rating-score').contents[0]
            name = html.find(itemprop='name').contents[0]
            playercount = html.find(class_='count-stats').contents[0]
            playercount = playercount[0: len(playercount)-4]
            game['tag'] = tagList
            game['score'] = score
            game['Gname'] = name
            game['playercount'] = playercount
            return game
        except Exception as e:
            return None



