# -*- coding: utf-8 -*- 

from Crypto.Cipher import AES
import base64

from module.constant import *

class MyCrypto:
    def __init__(self):
        BLOCK_SIZE = 32
        PADDING = '|'
        secret = "140b41b22a29beb4061bda66b6747e14"
        cipher = AES.new(secret)

        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

        self.encodeAES = lambda s: base64.b64encode(cipher.encrypt(pad(s)))
        self.decodeAES = lambda e: cipher.decrypt(base64.b64decode(e)).decode('utf-8').rstrip(PADDING)
        
def getSlackToken():
    return MyCrypto().decodeAES(SLACK_TOKEN)