from encodings import utf_8
import re
from urllib import request
from bs4 import BeautifulSoup
# from selenium import webdriver
# from selenium.webdriver.common.by import By
import time
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome import service as fs
import re
import csv
# import pandas as pd
# import glob
# from difflib import SequenceMatcher
# import socks, socket
import subprocess
# windowsの場合
# import chromedriver_binary
import requests
import lxml.html
# import codecs

class BasData:
    def __init__(self):
        self.proxies = {
            'http': 'socks5://localhost:9050',
            'https': 'socks5://localhost:9050'
        }
        with open('./バス路線.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['会社名', '路線名', 'バス停名', '緯度', '経度'])
        self.csv_file = open("./人力データ収集 - バス会社url.csv", "r", encoding="utf-8")
        self.f = csv.reader(self.csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        self.err_msg = None
    def get_routes_url(self, company_url, i):
        print(company_url,i)
        url = 'https://www.navitime.co.jp/bus/route/{}/&p={}'.format(company_url,i)
        res = requests.get(url, proxies=self.proxies)
        soup = BeautifulSoup(res.content, 'html.parser')
        self.err_msg = soup.find(id='error-message')
        if self.err_msg != None:
            return
        # print(self.err_msg)
        tags = soup.find('ul', id='bus-link-list').find_all('a', href=re.compile('^/bus/route/'))
        self.route_urls = []
        self.route_names = []
        for tag in tags:
            self.route_names.append(tag.string)
            self.route_urls.append(tag.get('href'))

    def bas_station_info(self, company,i):
        # print(self.route_names[i])
        url = 'https://www.navitime.co.jp' + self.route_urls[i]
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        tags = soup.find_all('dd', class_='node_frame')
        # print(tags[0]['data-lat'])
        self.data = []
        for tag in tags:
            self.data.append([company, self.route_names[i], tag['data-name'], tag['data-lat'], tag['data-lon']])
    
    def write_csv(self):
        try:
            with open('./バス路線.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerows(self.data)
        except:
            print('')
    
    def get_ip_address(self):
        ip = requests.get("https://www.cman.jp/network/support/go_access.cgi", proxies=self.proxies)
        s = BeautifulSoup(ip.content, 'html.parser')
        print(s)

    def tor(self, args):
        subprocess.call(args)


if __name__ == "__main__":
    bas_data = BasData()
    args = ['brew', 'services', 'start', 'tor']
    bas_data.tor(args)
    time.sleep(5)
    bas_data.get_ip_address()
    for company_url in bas_data.f:
        # bas_data.get_ip_address()
        bas_data.err_msg = None
        l = 0
        while bas_data.err_msg == None:
            l+=1
            bas_data.get_routes_url(company_url[1], l)
            for i in range(len(bas_data.route_urls)):
                bas_data.bas_station_info(company_url[0], i)
                bas_data.write_csv()
        args = ['brew', 'services', 'restart','tor']
        bas_data.tor(args)
        time.sleep(5)
    args = ['brew', 'services', 'stop', 'tor']
    bas_data.tor(args)
    bas_data.csv_file.close()