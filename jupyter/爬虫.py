#!/usr/bin/env python
# coding: utf-8
import json
import requests
import re
from requests.exceptions import RequestException
from multiprocessing import Pool #多进程pool

def get_one_page(url):
    try:
        mao = requests.get(url)
        if mao.status_code == 200:
            return mao.text
        return None
    except RequestException:
        return None
def parse_one_page(html):     #正则表达式重点 .*?  /s+  /d+  re.S
    pattcrn = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?class="name".*?">('
                         +'.*?)</a>.*?star">\n\s+(.*?)\n.*?releasetime">(.*?)</p>.*?"integer">('
                         +'.*?)</i><i.*?"fraction">(.*?)</i></p>.*?</dd>', re.S) 
    items = pattcrn.findall(html)
    for item in items:
        yield{                   #  yield 函数中迭代，反馈迭代一次结果
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5]+item[6]
        }
def to_file(content):
    with open('result.txt','a',encoding = 'utf-8')as f:          
        f.write(json.dumps(content,ensure_ascii = False)+'\n')  #转码json
        f.close()

def go(offset):
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        to_file(item)
if __name__ == '__main__':  #调用程序
##    for i in range(10):
##        go(i * 10)
    pool = Pool()
    pool.map(go,[i*10 for i in range(10)])   #pool.map(函数，数据列表)
