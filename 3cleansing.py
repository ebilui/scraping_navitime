import pandas as pd
import re
import csv
from sympy.geometry import Point, Polygon
import requests
import json

class V2City:
    def add_city(self):
        with open('./市区町村/3市区町村.csv', 'w', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['市区町村名', '緯度', '経度'])
        # bas_data = pd.read_csv('./csv/バス停.csv')
        bas_data = pd.read_csv('./市区町村/3.csv')
        self.df = pd.DataFrame(bas_data)
        self.lat_lon_arr = self.df[['緯度','経度']].values.tolist()
        for lat_lng in self.lat_lon_arr:
            V2City.reverse_geocoding(self, lat_lng[0], lat_lng[1])
    def reverse_geocoding(self, lat, lng):
        url = 'https://aginfo.cgk.affrc.go.jp/ws/rgeocode.php?json&lat='+str(lat)+'&lon='+str(lng)
        response = requests.get(url)
        json_resp = json.loads(response.text)
        try:
            print(str(lat) + ' ' + str(lng))
            print(json_resp)
            with open('./市区町村/3市区町村.csv', 'a', encoding='utf-8', newline="") as f:
                writer = csv.writer(f)
                writer.writerow([json_resp['result']['municipality']['mname'], lat, lng])
        except KeyError as err_message:
            print (err_message)
            print (str(lat) + ' ' + str(lng))
            with open('./市区町村/3市区町村.csv', 'a', encoding='utf-8', newline="") as f:
                writer = csv.writer(f)
                writer.writerow(['error', lat, lng])
            #look at https://www.finds.jp/rgeocode/index.html.ja


if __name__=='__main__':
      v2city = V2City()
      v2city.add_city()