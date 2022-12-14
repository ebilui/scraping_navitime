import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
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

def request(station_name, bas_company):
    url = 'https://mb.jorudan.co.jp/os/sp/bus/rosenbus.cgi?mode=sh&word={}'.format(station_name)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    try:
        tbody = soup.find('tbody')
        tr_tags = tbody.find_all('tr')
    except:
        print('error')
        return ['None']
    num = []
    company = []
    for tr in tr_tags:
        td = tr.find('td')
        com = td.get_text()
        if com in bas_company:
            a = tr.find('a')
            href = a.get('href')
            n = num_of_bus(href, driver)
            print(n)
            num.append(n)
            company.append(com)
        else:
            continue
    return {'バス停数':num, '会社名':company}
def num_of_bus(href, driver):
    # res = requests.get('https://mb.jorudan.co.jp/' + href)
    driver.set_page_load_timeout(3)
    driver.implicitly_wait(3)
    print(href)
    try:
        driver.get('https://mb.jorudan.co.jp/' + href)
        html = driver.page_source.encode('utf-8')
        driver.find_element(By.XPATH, '//*[@id="ZENRINMAP"]/div/div[5]/div[2]/div[1]/a/img')
        soup = BeautifulSoup(html, 'html.parser')
        pin = soup.find_all('img', attrs={'style':'z-index: 0; border-width: 0px; top: -290px; left: 0px; position: absolute;'})
        print(len(pin))
        return len(pin)
    except NoSuchElementException:
        print('no such element')
        return num_of_bus(href, driver)
    except TimeoutException:
        print('timeout')
        return num_of_bus(href, driver)

def output(line):
    with open('./csv/バス停数.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(line)


bas_company = ['都バス２３区','都バス多摩','東急バス','小田急バス','関東バス','西武バス','国際興業バス','京王バス','京王電鉄バス','京王バス小金井','京急バス','京成バス','京成タウンバス','東武バスセントラル','立川バス','西東京バス','神奈川中央交通','東京ＢＲＴ','ｋｍモビリティサービス','ウィラーエクスプレス','日立自動車交通','新日本観光自動車','銀河鉄道','大島バス','八丈町営バス','小笠原村営バス','千代田区コミュニティ','中央区コミュニティ','港区コミュニティ','文京区コミュニティ''台東区コミュニティ','墨田区コミュニティ','江東区コミュニティ','大田区コミュニティ','渋谷区コミュニティ','杉並区コミュニティ','北区コミュニティ','荒川区コミュニティ','板橋区コミュニティ','練馬区コミュニティ','武蔵野市コミュニティ','三鷹市コミュニティ','狛江市コミュニティ','小金井市コミュニティ','国分寺市コミュニティ','国立市コミュニティ','立川市コミュニティ','府中市コミュニティ','稲城市コミュニティ','西東京市コミュニティ','小平市コミュニティ','清瀬市コミュニティ','東村山市コミュニティ','武蔵村山市コミュニティ','東大和市コミュニティ','昭島市コミュニティ','羽村市コミュニティ','あきる野市コミュニティ','八王子市コミュニティ','町田市コミュニティ','日の出町コミュニティ']

get_name()
with open('./csv/バス停数.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['市区町村名','緯度','経度','区内バス停ID','バス会社名称','バス停名称','バス停数', 'サイトのバス会社名'])
try:
    driver = webdriver.Chrome()
    time.sleep(5)
    df = pd.read_csv('./csv/search_name.csv')
    lines = df.values.tolist()
    for line in lines:
        print(line)
        station_name = line[5]
        bus_dic = request(station_name, bas_company)
        for i in range(len(bus_dic['バス停数'])):
            bus_num = bus_dic['バス停数'][i]
            bus_com = bus_dic['会社名'][i]
            line+=[bus_num,bus_com]
            print(line)
            output(line)
            del line[-1]
            del line[-2]
finally:
    driver.quit()