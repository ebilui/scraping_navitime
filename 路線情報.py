import time
import requests
from bs4 import BeautifulSoup
import csv

class RosenJouhou:
    def __init__(self):
        with open('./test.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['会社名称', '路線名称', 'どこからどこまで', '行き方面', '帰り方面', 'バス停名称', 'url'])

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
            i=1
            still_page = True
            while still_page:
                print('still_page：'+str(still_page))
                print(i)
                res = RosenJouhou.search(self, 'https://mb.jorudan.co.jp'+href+'line/?page='+str(i))
                print(res.url)
                print('https://mb.jorudan.co.jp'+href+'line/')
                if str(res.url) != 'https://mb.jorudan.co.jp'+href+'line/':
                    RosenJouhou.search_by_rosen(self, res)
                    i+=1
                else:
                    print('over page')
                    still_page = False

    def search_by_rosen(self, res):
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table', class_='route-table')
        tbody = table.find('tbody')
        tr = tbody.find_all('tr')
        th_arr = tbody.find_all('th')
        for i in range(len(th_arr)):
            print(th_arr[i])
            td = tr[i].find_all('td')[1]
            a = th_arr[i].find('a')
            href = a.attrs.get('href')
            self.rosen = a.get_text()
            self.where_to_where = td.get_text()
            print(self.where_to_where)
            res = RosenJouhou.search('self', 'https://mb.jorudan.co.jp/'+href)
            RosenJouhou.get_stop_station(self, res)

    def get_stop_station(self, res):
        soup = BeautifulSoup(res.text, 'html.parser')
        ul = soup.find('ul', class_='route')
        li_arr = ul.find_all('li')
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
            url = []
            houmen = ''
            for l in range(len(stop_lines)):
                if stop_lines[l][i] == '':
                    continue
                if 'down' in stop_lines[l][i]:
                    houmen = 'down'
                    stop_lines[l][i] = stop_lines[l][i].replace(' down', '')
                else:
                    houmen = 'up'
                    stop_lines[l][i] = stop_lines[l][i].replace(' up', '')
                url.append('https://mb.jorudan.co.jp/'+li.find('a').attrs['href'])
                line.append(stop_lines[l][i])
            lines.append({houmen: [line,url]})
        RosenJouhou.output(self, lines)

    def output(self, lines):
        with open('./test.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for line in lines:
                houmen = list(line.keys())[0]
                values = list(line.values())[0]
                stations = values[0]
                urls = values[1]
                if houmen == 'down':
                    iki_houmen = stations[-1]+'方面'
                    hantai_houmen = stations[0]+'方面'
                else:
                    iki_houmen = stations[0]+'方面'
                    hantai_houmen = stations[-1]+'方面'
                for i in range(len(stations)):
                    writer.writerow([self.company, self.rosen, self.where_to_where, iki_houmen, hantai_houmen, stations[i], urls[i]])

if __name__ == '__main__':
    rosen_jouhou = RosenJouhou()
    rosen_jouhou.search_by_company()