# -*- coding: utf-8 -*- 

import requests
import json
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs

from module import util

def crawl(db_dir, proxies, verify, timeout=30):
  count = 0
  with requests.Session() as s:
    s.proxies = proxies
    s.verify = verify
    s.timeout = timeout
    with open(db_dir, 'r') as db:
      for line in db:
        name, link = line.strip().split(',')
        site = bs(s.get(link).text, 'html.parser')
        available = site.select_one('div.not_goods') is None and site.select_one('strong.title_error') is None
        if available:
          message = f"*{util.getTime()}*\n{name}\n> <{link}|구매하기>"
          util.postMessage(message=message, proxy=proxies['https'], icon=':mask:', username='마스크 알리미')
          s.post('https://maker.ifttt.com/trigger/free_emoticon/with/key/ce8QM-IDoL98p4TIyf9wSU', data={})
          count += 1
  print(f"Checked! {count} mask(s) available. {util.getTime()}")
