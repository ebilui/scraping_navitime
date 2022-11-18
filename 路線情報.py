import time
import requests
from bs4 import BeautifulSoup
import csv

class RosenJouhou:
    def __init__(self):
        with open('./test.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['会社名称', '路線名称', 'どこからどこまで', '行き方面', '帰り方面', 'バス停名称'])

    def search(self, url):
        res = requests.get(url)
        return res

    def search_by_company(self):
        url = 'https://mb.jorudan.co.jp/os/bus/tokyo/'
        res = RosenJouhou.search(self, url)
        soup = BeautifulSoup(res.text, 'html.parser')
        ul = soup.find('ul', class_='list-btn')
        li_arr = ul.find_all('li')
        for li in li_arr:
            a = li.find('a')
            self.company = a.get_text()
            href = a.attrs.get('href')
            res = RosenJouhou.search(self, 'https://mb.jorudan.co.jp/'+href)
            RosenJouhou.search_by_rosen(self, res)

    def search_by_rosen(self, res):
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table', class_='route')
        th_arr = table.find_all('th')
        for th in th_arr:
            a = th.find('a')
            href = a.attrs.get('href')
            self.rosen = a.get_text()
            res = RosenJouhou.search('self', 'https://mb.jorudan.co.jp/'+href)
            RosenJouhou.get_stop_station(self, res)

    def get_stop_station(self, res):
        soup = BeautifulSoup(res.text, 'html.parser')
        ul = soup.find('ul', class_='route')
        li_arr = ul.find_all('li')
        self.where_to_where = li_arr[1].find('a').get_text() + '~' + li_arr[-1].find('a').get_text()
        stop_lines = []
        i = 0
        for li in li_arr:
            if i==0:
                i+=1
                continue
            img_arr = li.find_all('img')
            stop_station = []
            for img in img_arr:
                station_name = li.find('a').get_text()
                if img.attrs['src'] == '/os/bus/images/down.png':
                    station_name += ' down'
                elif img.attrs['src'] == '/os/bus/images/up.png':
                    station_name += ' up'
                if img.attrs['alt'] == '停車':
                    stop_station.append(station_name)
                else:
                    stop_station.append('')
            stop_lines.append(stop_station)

        lines = []
        for i in range(len(stop_lines[0])):
            line = []
            houmen = ''
            if 'down' in stop_lines[0][i]:
                houmen = 'down'
            else:
                houmen = 'up'
            for l in range(len(stop_lines)):
                if stop_lines[l][i] == '':
                    continue
                print(stop_lines[0][i])
                if houmen == 'down':
                    stop_lines[l][i] = stop_lines[l][i].replace(' down', '')
                else:
                    stop_lines[l][i] = stop_lines[l][i].replace(' up', '')
                line.append(stop_lines[l][i])
            lines.append({houmen: line})
        RosenJouhou.output(self, lines)

    def output(self, lines):
        with open('./test.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for line in lines:
                houmen = list(line.keys())[0]
                stations = list(line.values())[0]
                if houmen == 'down':
                    iki_houmen = stations[-1]+'方面'
                    hantai_houmen = stations[0]+'方面'
                else:
                    iki_houmen = stations[0]+'方面'
                    hantai_houmen = stations[-1]+'方面'
                for station in stations:
                    writer.writerow([self.company, self.rosen, self.where_to_where, iki_houmen, hantai_houmen, station])

if __name__ == '__main__':
    rosen_jouhou = RosenJouhou()
    rosen_jouhou.search_by_company()