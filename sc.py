from encodings import utf_8
import re
from bs4 import BeautifulSoup
import time
import re
import csv
import subprocess
import requests
import sys

class BasDataMac:
    def __init__(self):
        self.proxies = {
            'http': 'socks5://localhost:9050',
            'https': 'socks5://localhost:9050'
        }
        with open('./バス路線.csv', 'w', newline="") as f:
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
            with open('./バス路線.csv', 'a', newline="") as f:
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

class BasDataWin:
    def __init__(self):
        self.proxies = {
            'http': 'socks5://localhost:9050',
            'https': 'socks5://localhost:9050'
        }
        self.headers_dic = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        with open('./バス路線.csv', 'w', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['会社名', '路線名', 'バス停名', '緯度', '経度'])
        self.csv_file = open("./人力データ収集 - バス会社url.csv", "r", encoding="utf-8")
        self.f = csv.reader(self.csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        self.exist = True

    def get_routes_url(self, company_url, i):
        try:
            url = 'https://www.navitime.co.jp/bus/route/{}/&p={}'.format(company_url,i)
            res = requests.get(url, proxies=self.proxies, headers=self.headers_dic)
            soup = BeautifulSoup(res.content, 'html.parser')
            tags = soup.find('ul', id='bus-link-list').find_all('a', href=re.compile('^/bus/route/'))
            self.route_urls = []
            self.route_names = []
            for tag in tags:
                self.route_names.append(tag.string)
                self.route_urls.append(tag.get('href'))
            print('success to get routes name : ' + str(self.route_names))
        except:
            self.exist = False

    def bas_station_info(self, company,i):
        try:
            url = 'https://www.navitime.co.jp' + self.route_urls[i]
            res = requests.get(url)
            soup = BeautifulSoup(res.content, 'html.parser')
            tags = soup.find_all('dd', class_='node_frame')
            print('success to get bas station data')
            self.data = []
            for tag in tags:
                self.data.append([company, self.route_names[i], tag['data-name'], tag['data-lat'], tag['data-lon']])
        except:
            sys.exit("ERROR : couldn't get bas station data")

    def write_csv(self):
        try:
            print('outputting data...')
            with open('./バス路線.csv', 'a', encoding='utf-8', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(self.data)
            print('success')
        except:
            sys.exit("ERROR : couldn't out put to csv file")

    def get_ip_address(self):
        try:
            print('-------------------------------------------------')
            print('\nyour IP address')
            proxies = {
                'https': 'socks5h://127.0.0.1:9050',
            }
            res = requests.get('https://icanhazip.com/', proxies=proxies)
            print(res.text)
            print('-------------------------------------------------')
        except:
            sys.exit("couldn't open the IP address site")

    def start_tor(self):
        print('starting Tor...')
        try:
            cmd = r".\tor-win32-0.4.7.10\Tor\tor.exe"
            self.p = subprocess.Popen(cmd, shell=False)
            print('success')
            time.sleep(5)
        except:
            sys.exit('start Tor error')

    def kill_tor(self):
        print('killing Tor...')
        try:
            self.p.kill()
            time.sleep(5)
            print('success')
        except:
            sys.exit('kill Tor error')


if __name__ == "__main__":
    print('start scraping')
    # macの場合
    # bas_data = BasDataMac()
    # windowsの場合
    bas_data = BasDataWin()
    for company_url in bas_data.f:
        bas_data.start_tor()
        bas_data.get_ip_address()
        print('company name : ' + company_url[0])
        bas_data.exist = True
        l = 0
        while bas_data.exist:
            l+=1
            is_page_exist = bas_data.get_routes_url(company_url[1], l)
            if bas_data.exist:
                print('--------------------------' + str(l) + 'page--------------------------')
                for i in range(len(bas_data.route_urls)):
                    print('getting ' + bas_data.route_names[i] + 'data...')
                    bas_data.bas_station_info(company_url[0], i)
                    bas_data.write_csv()
                print('--------------------------------------------------------------')
        bas_data.kill_tor()
    print("""all complete.
    finish scraping""")
    bas_data.csv_file.close()