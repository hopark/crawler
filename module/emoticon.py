# -*- coding: utf-8 -*- 

import requests
import json
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs

import util 

def crawl(db_dir, proxies, verify, timeout=30):
    count = 0
    post_list = open(db_dir, 'r').read().split("\n")
    with requests.Session() as s:
        s.proxies = proxies
        s.verify = verify
        s.timeout = timeout

        blog = bs(s.get('http://blog.naver.com/PostList.nhn?blogId=nova672&from=postList&categoryNo=32').text, 'html.parser')
        posts = blog.select('div#PostThumbnailAlbumViewArea > ul.thumblist > li.item')
        with open(db_dir, 'a') as db:
            for post in posts: 
                content = "[" + post.select_one('strong.title').text + "]<br>"
                post_link = "http://blog.naver.com" + post.select_one("a.link")["href"]
                post_id = parse_qs(urlparse(post_link).query)['logNo'][0]
                if post_id in post_list: break
                post_html = bs(s.get(post_link).text, 'html.parser')
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
                s.post('https://maker.ifttt.com/trigger/free_emoticon/with/key/ce8QM-IDoL98p4TIyf9wSU', data={'value1' : content, 'value2' : channel_link})
                print(content.replace('<br>', '\n'))
                print('채널로 이동 : ' + channel_link)
                print('+++++++++++++++++++++++++++++++++++++')
                db.write(post_id + "\n")
                count += 1
    if count == 0:
        print(f"추가 이모티콘 없음. {util.getDate()}")
