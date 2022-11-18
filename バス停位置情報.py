import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
import sys
import re

with open('./csv/乗換案内NEXT緯度経度バス停.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['会社名称','路線名称','どこからどこまで','行き方面','帰り方面','バス停名称','url','緯度','経度'])
file = open('./csv/乗換案内NEXT路線.csv', 'r', encoding='utf-8')
header = next(csv.reader(file))
reader = csv.reader(file)
for row in reader:
    res = requests.get(row[-1])
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find('table', class_='pole')
    tr_arr = table.find_all('tr')
    exist_or_not = []
    noriba = ''
    for tr in tr_arr:
        td = tr.find('td')
        a = td.find('a')
        if not row[1] in td.get_text():
            continue
        if not row[3] in td.get_text():
            print(a)
            if not row[4] in td.get_text():
                if not row[2] in td.get_text():
                    exist_or_not.append('no')
                    continue
        exist_or_not.append('exist')
        span = tr.find('span', class_='check')
        noriba = span.get_text()
        print(noriba)
    if not 'exist' in exist_or_not:
        print('ERROR: there is no station in list')
        sys.exit()
    script = soup.find_all('script')
    lan_lon_script = script[-1]
    lan_lon_script = lan_lon_script
    script_noriba_arr = re.findall(r"(?<=<br>)(.*)(?=</a>)", str(lan_lon_script))
    print(script_noriba_arr)
    lat = re.findall(r"(?<=\$\.jorudan\.addMarker\({'lat':)(.*)(?=,'lon')", str(lan_lon_script))
    lon = re.findall(r"(?<=,'lon':)(.*)(?=,'text')", str(lan_lon_script))
    i=0
    for script_noriba in script_noriba_arr:
        if noriba in script_noriba:
            break
        i+=1
    print(row[1]+'　'+row[-1])
    print(eval(lat[i])+0.00322)
    print(eval(lon[i])-0.00322)
    with open('./csv/乗換案内NEXT緯度経度バス停.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        row+=[eval(lat[i])+0.00322, eval(lon[i])-0.00322]
        writer.writerow(row)
file.close()