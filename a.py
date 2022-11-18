from encodings import utf_8
import re
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import chromedriver_binary
import time
import json

# user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
# options = webdriver.ChromeOptions()
# options.add_argument('--uer-agent='+user_agent)
res = requests.get('https://mb.jorudan.co.jp/os/bus/1301/line/4211.html')
print(res.text)

# print(json_load)
# print(json_load )
# driver = webdriver.Chrome(chrome_options=options)
# driver.get(url)
# time.sleep(20)
# html = driver.page_source.encode('utf-8')
# soup = BeautifulSoup(html, 'html.parser')
# print(soup)
# title_part = soup.find("script", {"type": "application/ld+json"})
# print(title_part)
# time.sleep(1000)



# --------------
# |緯度＋0.00322|
# |軽度ー0.00322|
# --------------