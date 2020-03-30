# -*- coding: utf-8 -*- 

import requests
import json
from requests.auth import HTTPBasicAuth
import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse, parse_qs
from apscheduler.schedulers.blocking import BlockingScheduler
from time import gmtime, strftime
import os

DB_DIR = os.path.dirname(os.path.abspath(__file__)) + 'masks'

sched = BlockingScheduler()
proxyDict = { 
              "http"  : "http://10.112.1.184:8080/", 
              "https" : "http://10.112.1.184:8080/", 
              "ftp"   : "ftp://10.112.1.184:8080/"
            }
warnings.simplefilter('ignore',InsecureRequestWarning)

def getMask():
  f = open(DB_DIR, 'r')
  count = 0
  with requests.Session() as s:
    for line in f:
      name, link = line.strip().split(',')
      site = bs(s.get(link, proxies=proxyDict, verify=False).text, 'html.parser')
      available = site.select_one('div.not_goods') is None and site.select_one('strong.title_error') is None
      if available:
        s.post('https://maker.ifttt.com/trigger/free_emoticon/with/key/ce8QM-IDoL98p4TIyf9wSU', data={'value1' : '마스크 구매 : ' + name , 'value2' : link}, proxies=proxyDict, verify=False)
        count += 1
  print(f"Checked! {count} mask(s) available. {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")
  f.close()

sched.add_job(getMask, 'interval', seconds=1, max_instances=5)
sched.start()

