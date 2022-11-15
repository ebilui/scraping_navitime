# coding: UTF-8

import pandas as pd
import re
import csv
import mojimoji
import shapefile
from sympy.geometry import Point, Polygon
import time

class Cleansing:
    def __init__(self):
        self.cp_id_dec = {}
        with open('./csv/バス会社一覧.csv','r', encoding='utf-8') as f:
            next(csv.reader(f))
            companies = csv.reader(f, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
            for company in companies:
                self.cp_id_dec[company[1]] = company[0]

    def company(self):
        to_company = {'京成バス/京成タウンバス':'京成バス（株）', '都営バス/京王バス':'都営バス', '日立自動車交通':'日立自動車交通', '国際興業バス':'国際興業（株）', 'ＣｏＣｏバス':'小金井市', 'めぐりん(台東区)':'台東区', 'ぶんバス(国分寺市)':'国分寺市', 'グリーンバス':'東村山市', '京急バス':'京成バス（株）', 'にじバス':'小平市', 'さくら(葛飾区)':'葛飾区', 'ウィラー(高速バス)':'高速バス', 'ちゅうバス':'府中市', 'Aバス(昭島市)':'昭島市', '関越交通':'関越交通（株）', 'くにっこ':'国立市', '板橋区コミュニティバス':'板橋区', 'ぐるりーんひのでちゃん':'日出町', 'コミュニティ交通(江戸川区)':'江戸川区', '船橋新京成バス':'船橋新京成バス', '国際興業バス/関東バス':'関東バス（株）', 'ＶＩＰライナー(高速バス)':'高速バス', 'さくら高速バス(高速バス)':'高速バス', '東急/ちばシティ/トランジット/京王':'京成トランジットバス', '千葉みらい観光バス(高速バス)':'高速バス', '高速バス':'高速バス', 'Dts creation(高速バス)':'高速バス', 'お台場レインボーバス':'NULL', '三宅村営バス':'三宅村', '青木バス(高速バス)':'高速バス', '京王バス/小田急バス':'京王バス', 'キラキラ号(高速バス)':'高速バス', '臨港バス':'川崎鶴見臨港バス', '千葉みらい観光/三栄交通(高速バス)':'高速バス', '小湊鉄道/東京バス':'小湊鉄道', 'やまびこ号(檜原村)':'檜原村', '風ぐるま(千代田区)':'千代田区', '東京富士交通(高速バス)':'高速バス', '西武バス/立川バス':'西武バス（株）', '中日本ツアーバス(高速バス)':'高速バス', '銀河鉄道':'銀河鉄道（株）', '東急トランセ':'東急バス・東急トランセ', 'MMシャトル(武蔵村山市)':'武蔵村山市', 'ちばグリーンバス':'ちばグリーンバス', 'オリオンバス(高速バス)':'高速バス', '関東鉄道':'関東鉄道（株）', '東武バス':'東武バス', '山一サービス/武井観光(高速バス)':'高速バス', '八丈町営バス':'八丈町', 'くるりんバス':'日進市', '小笠原村営バス':'小笠原村', '神姫観光バス(高速バス)':'高速バス', '小湊鉄道':'小湊鉄道', '足立区社会実験バス':'足立区', '大新東バス(高速バス)':'高速バス', '東急バス':'東急バス（株）', '京成トランジットバス/京王バス東':'京成トランジットバス', '瑞穂町コミュニティバス':'瑞穂町', 'みどりバス':'練馬区', '昌栄交通(高速バス)':'高速バス', '関越交通/川越観光自動車':'関越交通（株）', '都営バス/京成タウンバス':'都営バス', 'ユタカ交通(高速バス)':'高速バス', '成田空港交通':'成田空港交通', '千葉中央バス':'千葉中央バス', '西武バス':'西武バス（株）', 'にいバス(新座市)':'新座市', '京成バス/小湊鐵道':'小湊鉄道', 'IKEBUS':'豊島区', '岩手県北バス(高速バス)':'高速バス', '高知駅前観光(高速バス)':'高速バス', '会津バス(高速バス)':'高速バス', 'CoCoバス(小金井市)［野川・七軒家循環］':'小金井市', 'グレース観光バス(高速バス)':'高速バス', 'ユタカコーポレーション(高速バス)':'高速バス', 'ちぃばす':'港区', 'ちょこバス':'東大和市', 'アウル交通(高速バス)':'高速バス', 'フジエクスプレス':'高速バス', 'すぎ丸':'杉並区', 'サンシャインエクスプレス(高速バス)':'高速バス', '西東京バス':'西東京バス（株）', '武井観光(高速バス)':'高速バス', '泉観光バス(高速バス)':'高速バス', '京成タウンバス/マイスカイ交通':'京成タウンバス', '京成/トラン/国際興業':'京成トランジットバス', '千葉内陸バス':'千葉内陸バス', '琴平バス(高速バス)':'高速バス', 'しなバス':'品川区', 'パリポリくんバス':'草加市', '小田急バス':'小田急バス（株）', '日野市ミニバス':'日野市', '西武バス/国際興業バス':'西武バス（株）', 'はなバス':'西東京市', '村営バス(神津島村)':'神津島村', '杉崎観光バス(高速バス)':'高速バス', '新宿WEバス':'京王バス', '朝日バス':'朝日バス', '江戸バス(中央区)':'中央区', 'ハチ公バス':'渋谷区', '関東バス':'関東バス（株）', '平和交通':'平和交通', '平和交通/あすか交通':'平和交通', '広栄交通バス(高速バス)':'高速バス', 'JRバス関東':'JRバス関東（株）', 'かわせみ号':'町田市', 'Bーぐる(文京区)':'文京区', '京成バス':'京成バス（株）', '都営バス':'都営バス', '東急バス/小田急バス':'東急バス（株）', '京王バス/神奈川中央交通':'京王バス', '新島村コミュニティバス':'新島村', '海部観光(高速バス)':'高速バス', 'るのバス':'西東京バス（株）', '日の丸自動車':'日の丸自動車興業', 'かわせみゴー':'日野市', '西武バス/関東バス':'西武バス（株）', '新日本観光自動車':'足立区', 'ぶるべー号':'小平市', 'ウエスト観光バス(高速バス)':'高速バス', 'さくら観光バス(高速バス)':'高速バス', 'ジャムジャムライナー(高速バス)':'高速バス', 'はちバス':'西東京バス（株）', '大島バス':'大島旅客自動車（株）', 'きよバス':'清瀬市', 'しおかぜ':'江東区', 'シャトルバス':'NULL', '立川バス':'立川バス（株）', '天領バス(高速バス)':'高速バス', '神奈川中央交通':'神奈川中央交通（株）', 'みんななかまバス':'川口市', '小田急バス/神奈川中央交通':'小田急バス（株）', 'ところバス':'所沢市', 'レインボーかつしか(葛飾区)':'葛飾区', '夜間温泉巡回バス(神津島村)':'神津島村', '京王バス/関東バス':'京王バス', '京王バス':'京王バス', 'Kバス(北区)':'北区', '多摩市ミニバス':'多摩市', 'はむらん':'羽村市'}
        csv_file = open("./csv/バス路線_before.csv", "r", encoding="utf-8")
        bas_data_arr = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
        i = 0
        company = []
        error = []
        for bas_data in bas_data_arr:
            if i==0:
                i+=1
                continue
            route = bas_data[1]
            key = re.findall('(?<=\[).+?(?=\])', route)[-1]
            if key in to_company:
                fix_company = to_company[key]
                bas_data[0] = fix_company
                company.append(bas_data)
                i+=1
            else:
                error.append(bas_data)
        with open('./csv/バス路線.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['バス会社名称','路線名称','バス停名称','緯度','経度'])
            writer.writerows(company)
        csv_file.close()

    def zen_to_han(self):
        bas_data = pd.read_csv('./csv/バス路線.csv')
        df = pd.DataFrame(bas_data)
        df['路線名称'] = df['路線名称'].apply(mojimoji.zen_to_han, kana=False)
        df['バス停名称'] = df['バス停名称'].apply(mojimoji.zen_to_han, kana=False)
        df.to_csv('./csv/バス路線.csv', index=False)

    def route(self):
        bas_data = pd.read_csv('./csv/バス路線.csv')
        df = pd.DataFrame(bas_data)
        print(df.duplicated(subset=['路線名称']).sum())
        df.drop_duplicates(subset=['路線名称'], inplace=True)
        for cp_id in self.cp_id_dec:
            df.loc[df['バス会社名称']==cp_id, 'バス会社ID'] = self.cp_id_dec[cp_id]
        df.drop(['バス会社名称', 'バス停名称', '緯度', '経度'], axis=1)
        serial_num = pd.RangeIndex(start=1, stop=len(df.index) + 1, step=1)
        df['路線ID'] = serial_num
        df = df.loc[:, ['路線ID', 'バス会社ID', '路線名称']]
        df.to_csv('./csv/路線.csv', index=False)

    def lan_lon(self):
        bas_data = pd.read_csv('./csv/バス路線.csv')
        df = pd.DataFrame(bas_data)
        print(df.duplicated(subset=['緯度', '経度', 'バス停名称']).sum())
        df.drop_duplicates(subset=['緯度', '経度', 'バス停名称'], inplace=True)
        df.drop('路線名称', axis=1)
        df = df.replace('\(.+?\)', {'バス停名称':''}, regex=True)
        df.sort_values(by='バス停名称', inplace=True)
        serial_num = pd.RangeIndex(start=1, stop=len(df.index) + 1, step=1)
        df['バス停ID'] = serial_num
        df = df.loc[:, ['バス停ID', 'バス会社名称', 'バス停名称', '緯度', '経度']]
        df.to_csv('./csv/ver.2バス停.csv', index=False)
    
    def join(self):
        df = pd.read_csv('./csv/バス路線.csv', encoding='utf-8')
        df2 = pd.read_csv('./csv/バス停.csv', encoding='utf-8')
        df3 = pd.read_csv('./csv/路線.csv', encoding='utf-8')

        # universitiesのIDを学校IDという名前に変更する
        # df2_ = df2.rename(columns={'ID': '学校ID'})
        df2 = df2.drop(["バス停名称","バス会社名称"],axis=1)

        # 学校IDというキーを元にして２つのCSVを結合する
        df_merged = pd.merge(df, df2, on=['緯度','経度'], how='left')
        df_merged = pd.merge(df_merged, df3, on='路線名称', how='left')

        df_merged.to_csv("./csv/merged.csv", index=False)

class City:
    def add_city(self):
        with open('./csv/市区町村バス停.csv', 'w', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['バス停ID', 'バス会社名称', 'バス停名称', '緯度', '経度', '市区町村名'])
        # bas_data = pd.read_csv('./csv/バス停.csv')
        bas_data = pd.read_csv('./バス停.csv')
        self.df = pd.DataFrame(bas_data)
        self.lat_lon_arr = self.df[['緯度','経度']].values.tolist()
        Cleansing.get_cities(self)

    def get_cities(self):
        src=shapefile.Reader('./japan_ver84/japan_ver84.shp',encoding='SHIFT-JIS')
        SRS=src.shapeRecords()
        i = 0
        for lat_lon in self.lat_lon_arr:
            print(i)
            print(lat_lon)
            time_sta = time.time()
            LONG=lat_lon[1]
            LAT=lat_lon[0]
            RPOINT=Point(LONG,LAT)
            for srs in SRS:
                shp=srs.shape
                rec=srs.record
                box=shp.bbox
                if box[0]<LONG<box[2] and box[1]<LAT<box[3]:  
                    pnt=shp.points
                    points=[]
                    for pp in pnt:   
                        points.append((pp[0],pp[1]))
                    poly=Polygon(*points)
                    #
                    if poly.encloses_point(RPOINT):
                        self.city = rec[5]
                        Cleansing.write_csv(self)
                        break
            time_end = time.time()
            tim = time_end - time_sta
            print('処理時間 : ' + str(tim))
            i+=1

    def write_csv(self):
        with open('./csv/市区町村バス停.csv', 'a', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow([self.city])


if __name__=='__main__':
    is_city_function = input("""処理をしたい方を入力してください。
    1  データクレンジング
    2  市区町村取得
    3  
    :""")
    if int(is_city_function) == 1:
        cleansing = Cleansing()
        # cleansing.company()
        # cleansing.zen_to_han()
        # cleansing.route()
        cleansing.lan_lon()
        # cleansing.join()
    else:
        city = City()
        city.add_city()