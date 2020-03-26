# -*- coding: utf-8 -*- 

import requests
import json
from requests.auth import HTTPBasicAuth
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs
from apscheduler.schedulers.blocking import BlockingScheduler
from time import strftime, gmtime

sched = BlockingScheduler()
DB_DIR = '/home/changho/Github/scrape/kakao/post'
proxyDict = { 
              "http"  : "http://10.112.1.184:8080/", 
              "https" : "http://10.112.1.184:8080/", 
              "ftp"   : "ftp://10.112.1.184:8080/"
            }

def getText(select):
    return ' '.join(select.text.split()).replace('"', "'") 

def getTextBySeletor(html, selector):
    return getText(html.select(selector)[0])

warnings.simplefilter('ignore',InsecureRequestWarning)
def checkEmoticon():
    post_db = open(DB_DIR, 'a')
    count = 0
    with requests.Session() as s:
        blog = bs(s.get('http://blog.naver.com/PostList.nhn?blogId=nova672&from=postList&categoryNo=32', proxies=proxyDict, verify=False).text, 'html.parser')
        posts = blog.select('div#PostThumbnailAlbumViewArea > ul.thumblist > li.item')
        for post in posts: 
            content = "[" + post.select_one('strong.title').text + "]<br>"
            post_link = "http://blog.naver.com" + post.select_one("a.link")["href"]
            post_id = parse_qs(urlparse(post_link).query)['logNo'][0]
            if post_id in open(DB_DIR, 'r').read(): break
            post_html = bs(s.get(post_link, proxies=proxyDict, verify=False).text, 'html.parser')
            components = post_html.select("div.se-main-container > div.se-component")
            channel_link = ""
            for component in components:
                if 'se-quotation' in component['class'] and 'se-1-quotation_line' not in component['class']:
                    content += "<br>".join([p.text for p in component.select('div.se-module > p')])
                    break
            for component in components:
                if 'se-image' in component['class']:
                    channel_link = json.loads(component.select_one('a.se-module')['data-linkdata'])['link']
                    if channel_link.count('/') == 3 and 'pf.kakao.com' in channel_link and '_xdNWYM' not in channel_link: break
            s.post('https://maker.ifttt.com/trigger/free_emoticon/with/key/ce8QM-IDoL98p4TIyf9wSU', data={'value1' : content, 'value2' : channel_link}, proxies=proxyDict, verify=False)
            print(content.replace('<br>', '\n'))
            print('채널로 이동 : ' + channel_link)
            print('+++++++++++++++++++++++++++++++++++++')
            post_db.write(post_id + "\n")
            count += 1
    post_db.close()
    if count == 0:
        print(f"추가 이모티콘 없음. {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")

sched.add_job(checkEmoticon, 'interval', minutes=5)
sched.start()
