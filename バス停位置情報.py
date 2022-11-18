import requests
import pandas as pd
from bs4 import BeautifulSoup
import csv
import sys
import re

file = open('./waaaa.csv', 'r', encoding='utf-8')
header = next(csv.reader(file))
reader = csv.reader(file)
i = 0
for row in reader:
    if i == 1:
        break
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
    print(noriba)
    for script_noriba in script_noriba_arr:
        if noriba in script_noriba:
            break
        i+=1
    print(lat[i])
    print(lon[i])
    # model_data = model_data.group(1)
    i+=1