# -*- coding: utf-8 -*- 

from time import gmtime, strftime
from constant import *
import os

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
  db_dir = os.path.dirname(os.path.abspath(__file__)) + '../db/'
  if app == "mask": return db_dir + MASK_DB
  elif app == "emoticon": return db_dir + EMOTICON_DB
  else: return None