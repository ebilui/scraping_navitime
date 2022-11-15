import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import mojimoji
import csv
import numpy as np
import time

def get_name():
    df = pd.read_csv('./csv/区内バス停.csv')
    df.drop_duplicates(subset='バス停名称', inplace=True)
    df['バス停名称'] = df['バス停名称'].apply(mojimoji.han_to_zen, kana=False)
    df.to_csv('./csv/search_name.csv', index=False)

def request(station_name):
    try:
        url = 'https://mb.jorudan.co.jp/os/sp/bus/rosenbus.cgi?mode=sh&word={}'.format(station_name)
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        tbody = soup.find('tbody')
        tr = tbody.find_all('tr')
        if len(tr) != 1:
            return
        a = tr[0].find('a')
        href = a.get('href')
        return href
    except:
        return
def num_of_bus(href, driver):
    print(1)
    # res = requests.get('https://mb.jorudan.co.jp/' + href)
    for _ in range(3):
        time.sleep(2)
        driver.set_page_load_timeout(5)
        try:
            driver.get('https://mb.jorudan.co.jp/' + href)
            print(2)
            html = driver.page_source.encode('utf-8')
            print(3)
            soup = BeautifulSoup(html, 'html.parser')
            print(4)
            pin = soup.find_all('img', attrs={'style':'z-index: 0; border-width: 0px; top: -290px; left: 0px; position: absolute;'})
            print(5)
            return len(pin)
        except TimeoutError:
            pass

def output(line):
    with open('./csv/バス停数.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(line)


get_name()
with open('./csv/バス停数.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['市区町村名','緯度','経度','区内バス停ID','バス会社名称','バス停名称','バス停数'])
driver = webdriver.Chrome()
df = pd.read_csv('./csv/search_name.csv')
lines = df.values.tolist()
for line in lines:
    print(line)
    station_name = line[5]
    href = request(station_name)
    print(href)
    if href != None:
        bus_num = num_of_bus(href, driver)
    else:
        bus_num = 'None'
    line.append(bus_num)
    output(line)
    # time.sleep(1.5)
driver.execute()