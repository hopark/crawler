# -*- coding: utf-8 -*- 

from time import gmtime, strftime
import slack
import os

from module.constant import *

def getTime():
  return strftime('%Y-%m-%d %H:%M:%S', gmtime())

def getDate():
  return strftime('%Y-%m-%d', gmtime())

def getProxies(place):
  if place == "suwon": ip = SUWON_IP
  elif place == "seoul": ip = SEOUL_IP
  else: return {}

  return { 
              "http"  : f"http://{ip}/", 
              "https" : f"http://{ip}/", 
              "ftp"   : f"ftp://{ip}/"
            }

def getDbDir(app):
  db_dir = os.path.dirname(os.path.abspath(__file__)) + '/../db'
  if app == "mask": return f"{db_dir}/{MASK_DB}"
  elif app == "emoticon": return f"{db_dir}/{EMOTICON_DB}"
  else: return None

def postMessage(message, proxy, icon, username):
  client = slack.WebClient(token=SLACK_TOKEN, proxy=proxy)
  client.chat_postMessage(channel=SLACK_CHANNEL, text=message, icon_emoji=icon, mrkdwn=True, username=username)