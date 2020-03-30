# -*- coding: utf-8 -*- 

import warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from apscheduler.schedulers.blocking import BlockingScheduler
import argparse

from module import util, emoticon, mask

parser = argparse.ArgumentParser(description='Crawler')
parser.add_argument('app', help='App name', type=str.lower, choices=['emoticon', 'mask'])
parser.add_argument('--proxy', '-p', help='Set proxy for company', default='', type=str, choices=['suwon', 'seoul'])
args = parser.parse_args()
app_name = args.app

db = util.getDbDir(args.app)
proxies = util.getProxies(args.proxy)

sched = BlockingScheduler()
warnings.simplefilter('ignore',InsecureRequestWarning)

if app_name == 'emoticon': 
    sched.add_job(lambda: emoticon.crawl(db=db, proxies=proxies, verify=False), 'interval', minutes=5)
elif app_name == 'mask':
    sched.add_job(lambda: mask.crawl(db_dir=db, proxies=proxies, verify=False), 'interval', seconds=1, max_instances=5)
else:
    exit(1)

sched.start()