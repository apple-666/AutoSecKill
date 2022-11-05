from datetime import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import os
import yaml
from time import sleep
from pykeyboard import *
import requests as requests


class timeTaobao(object):
    r1 = requests.get(url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',
                      headers={
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'})
    x = eval(r1.text)
    timeNum = int(x['data']['t'])

    def funcname():
        timeStamp = float(timeTaobao.timeNum) / 1000
        ret_datetime = datetime.utcfromtimestamp(timeStamp).strftime("%Y-%m-%d %H:%M:%S.%f")

        return ret_datetime


# t = timeTaobao.funcname()
# t2 = timeTaobao.funcname()
# if t2 > t:
#     print('更大')
# t = '1'
print(datetime.now())

# print(t)
# print('now:')
print(datetime.now())
