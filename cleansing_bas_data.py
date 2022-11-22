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
        bas_data = pd.read_csv('./csv/バス会社一覧.csv')
        self.company_df = pd.DataFrame(bas_data)
        self.company_df.to_csv('./乗換NEXT全データ/バス会社.csv', index=False)

    def company(self):
        to_company = {'都バス２３区':'都営バス','都バス多摩':'多摩市','東急バス':'東急バス（株）','小田急バス':'小田急バス（株）','関東バス':'関東バス（株）','西武バス':'西武バス（株）','国際興業バス':'国際興業（株）','京王バス':'京王バス','京王電鉄バス':'京王電鉄バス','京王バス小金井':'京王バス','京急バス':'京急バス','京成バス':'京成バス（株）','京成タウンバス':'京成タウンバス','東武バスセントラル':'東武バスセントラル','立川バス':'立川バス（株）','西東京バス':'西東京バス（株）','神奈川中央交通':'神奈川中央交通（株）','東京ＢＲＴ':'東京ＢＲＴ','ｋｍモビリティサービス':'ｋｍモビリティサービス','ウィラーエクスプレス':'ウィラーエクスプレス','日立自動車交通':'日立自動車交通','新日本観光自動車':'新日本観光自動車','銀河鉄道':'銀河鉄道（株）','大島バス':'大島旅客自動車（株）','八丈町営バス':'八丈町','小笠原村営バス':'小笠原村','千代田区コミュニティ':'千代田区','中央区コミュニティ':'中央区','港区コミュニティ':'港区','文京区コミュニティ':'文京区','台東区コミュニティ':'台東区','墨田区コミュニティ':'墨田区','江東区コミュニティ':'江東区','大田区コミュニティ':'大田区','渋谷区コミュニティ':'渋谷区','杉並区コミュニティ':'杉並区','北区コミュニティ':'北区','荒川区コミュニティ':'荒川区','板橋区コミュニティ':'板橋区','練馬区コミュニティ':'練馬区','武蔵野市コミュニティ':'武蔵野市','三鷹市コミュニティ':'三鷹市','狛江市コミュニティ':'狛江市','小金井市コミュニティ':'小金井市','国分寺市コミュニティ':'国分寺市','国立市コミュニティ':'国立市','立川市コミュニティ':'立川市','府中市コミュニティ':'府中市','城市コミュニティ':'城市','西東京市コミュニティ':'西東京市','小平市コミュニティ':'小平市','清瀬市コミュニティ':'清瀬市','東村山市コミュニティ':'東村山市','武蔵村山市コミュニティ':'武蔵村山市','東大和市コミュニティ':'東大和市','昭島市コミュニティ':'昭島市','羽村市コミュニティ':'羽村市','あきる野市コミュニティ':'あきる野市','八王子市コミュニティ':'八王子市','町田市コミュニティ':'町田市','日の出町コミュニティ':'日出町'}
        bas_data = pd.read_csv('./csv/乗換案内NEXT路線.csv')
        df = pd.DataFrame(bas_data)
        df = df.replace({'バス会社名称':to_company})
        self.company_id_df = pd.merge(df, self.company_df, on=['バス会社名称'], how='left')
        # self.company_id_df = df.loc[:, ['バス会社ID','バス停名称','路線名称']]

    def rosen(self):
        bas_data = pd.read_csv('./csv/乗換案内NEXT路線.csv')
        df = pd.DataFrame(bas_data)
        df.drop_duplicates(subset=['路線名称','どこからどこまで','行き方面','帰り方面'], inplace=True)
        serial_num = pd.RangeIndex(start=1, stop=len(df.index) + 1, step=1)
        df['路線ID'] = serial_num
        df = df.loc[:, ['路線ID','路線名称','どこからどこまで','行き方面','帰り方面']]
        self.rosen_id_df = pd.merge(self.company_id_df, df, how='left', on=['路線名称','どこからどこまで','行き方面','帰り方面'])
        rosen = self.rosen_id_df.loc[:, ['路線ID','バス会社ID','路線名称']]
        rosen = rosen.drop_duplicates(subset=['路線ID','バス会社ID','路線名称'])
        rosen.to_csv('./乗換NEXT全データ/路線名.csv', index=False)

    def bastei_id(self):
        bas_data = pd.read_csv('./csv/乗換案内NEXTバス停一覧.csv')
        df = pd.DataFrame(bas_data)
        df = df.loc[:, ['バス停ID', '緯度', '経度', 'バス停名称']]
        self.bastei_id_df = pd.merge(self.rosen_id_df, df, how='left', on=['緯度','経度', 'バス停名称'])
        i=1
        # l=1
        serial_num = []
        route_station = []
        while ((self.bastei_id_df['路線ID']==i).sum()) != 0:
            rosen = self.bastei_id_df[self.bastei_id_df['路線ID']==i]
            rosen_meisyou = rosen['路線名称']
            houmen = re.findall(r'(.*)方面',rosen['行き方面'].iloc[0])
            from_where = re.findall(r'(.*)～',rosen['どこからどこまで'].iloc[0])
            to_where = re.findall(r'～(.*)',rosen['どこからどこまで'].iloc[0])
            # print(rosen['どこからどこまで'].iloc[0])
            # print(from_where)
            # print(to_where)
            # print(self.bastei_id_df.loc[self.bastei_id_df.路線ID==i, '路線名称'])
            if houmen[0] != rosen['バス停名称'].iloc[0]:
                self.bastei_id_df.loc[self.bastei_id_df['路線ID']==i, '路線名称'] = self.bastei_id_df.loc[self.bastei_id_df['路線ID']==i, '路線名称'].replace(rosen_meisyou+'['+rosen['バス停名称'].iloc[0]+']')
            elif rosen['バス停名称'].iloc[0] == rosen['バス停名称'].iloc[-1]:
                self.bastei_id_df[self.bastei_id_df['路線ID']==i]['路線名称'] = rosen['路線名称'].replace(rosen_meisyou+'['+to_where[0]+']')
            else:
                # print(self.bastei_id_df.路線ID[self.bastei_id_df.路線ID==i])
                self.bastei_id_df[self.bastei_id_df.路線ID==i] = self.bastei_id_df.loc[self.bastei_id_df.路線ID==i].iloc[::-1]
                self.bastei_id_df.loc[self.bastei_id_df.路線ID==i, '路線名称'] = self.bastei_id_df.loc[self.bastei_id_df['路線ID']==i,'路線名称'].replace(rosen_meisyou+'['+self.bastei_id_df.loc[self.bastei_id_df.路線ID==i,'バス停名称'].iloc[-1]+']')
                print(self.bastei_id_df.loc[self.bastei_id_df.路線ID==i])
                # print(self.bastei_id_df.loc[self.bastei_id_df.路線ID==i])
            # route_station += rosen.to_dict()
            serial_num += list(range(1, (self.bastei_id_df['路線ID']==i).sum()+1, 1))
            # l+=rosen.sum()
            i+=1
        self.bastei_id_df['停車順番'] = serial_num
        # df = df.loc[:, ['路線ID', '停車順番', 'バス会社ID', 'バス停ID', 'バス停名称', '路線名称']]
        # df.to_csv('./csv/路線データ.csv', index_label='ID')
        self.bastei_id_df = self.bastei_id_df.loc[:, ['路線ID','停車順番','バス会社ID','バス停ID','バス停名称','路線名称']]
        self.bastei_id_df.to_csv('./乗換NEXT全データ/路線データ.csv', index=False)

    # def zen_to_han(self):
    #     bas_data = pd.read_csv('./csv/バス路線.csv')
    #     df = pd.DataFrame(bas_data)
    #     df['路線名称'] = df['路線名称'].apply(mojimoji.zen_to_han, kana=False)
    #     df['バス停名称'] = df['バス停名称'].apply(mojimoji.zen_to_han, kana=False)
    #     df.to_csv('./csv/バス路線.csv', index=False)

    # def route(self):
    #     bas_data = pd.read_csv('./csv/バス路線.csv')
    #     df = pd.DataFrame(bas_data)
    #     print(df.duplicated(subset=['路線名称']).sum())
    #     df.drop_duplicates(subset=['路線名称'], inplace=True)
    #     for cp_id in self.cp_id_dec:
    #         df.loc[df['バス会社名称']==cp_id, 'バス会社ID'] = self.cp_id_dec[cp_id]
    #     df.drop(['バス会社名称', 'バス停名称', '緯度', '経度'], axis=1)
    #     serial_num = pd.RangeIndex(start=1, stop=len(df.index) + 1, step=1)
    #     df['路線ID'] = serial_num
    #     df = df.loc[:, ['路線ID', 'バス会社ID', '路線名称']]
    #     df.to_csv('./csv/路線.csv', index=False)

    # def lan_lon(self):
    #     bas_data = pd.read_csv('./csv/バス路線.csv')
    #     df = pd.DataFrame(bas_data)
    #     print(df.duplicated(subset=['緯度', '経度', 'バス停名称']).sum())
    #     df.drop_duplicates(subset=['緯度', '経度', 'バス停名称'], inplace=True)
    #     df.drop('路線名称', axis=1)
    #     df = df.replace('\(.+?\)', {'バス停名称':''}, regex=True)
    #     df.sort_values(by='バス停名称', inplace=True)
    #     serial_num = pd.RangeIndex(start=1, stop=len(df.index) + 1, step=1)
    #     df['バス停ID'] = serial_num
    #     df = df.loc[:, ['バス停ID', 'バス会社名称', 'バス停名称', '緯度', '経度']]
    #     df.to_csv('./csv/ver.2バス停.csv', index=False)
    
    # def join(self):
    #     df = pd.read_csv('./csv/バス路線.csv', encoding='utf-8')
    #     df2 = pd.read_csv('./csv/バス停.csv', encoding='utf-8')
    #     df3 = pd.read_csv('./csv/路線.csv', encoding='utf-8')

    #     # universitiesのIDを学校IDという名前に変更する
    #     # df2_ = df2.rename(columns={'ID': '学校ID'})
    #     df2 = df2.drop(["バス停名称","バス会社名称"],axis=1)

    #     # 学校IDというキーを元にして２つのCSVを結合する
    #     df_merged = pd.merge(df, df2, on=['緯度','経度'], how='left')
    #     df_merged = pd.merge(df_merged, df3, on='路線名称', how='left')

    #     df_merged.to_csv("./csv/merged.csv", index=False)

class City:
    def add_city(self):
        with open('./csv/市区町村バス停.csv', 'w', encoding='utf-8', newline="") as f:
            writer = csv.writer(f)
            writer.writerow(['バス停ID', 'バス会社名称', 'バス停名称', '緯度', '経度', '市区町村名'])
        # bas_data = pd.read_csv('./csv/バス停.csv')
        bas_data = pd.read_csv('./csv/乗換案内NEXTバス停一覧.csv')
        self.df = pd.DataFrame(bas_data)
        self.lat_lon_arr = self.df[['緯度','経度']].values.tolist()
        City.get_cities(self)

    def get_cities(self):
        src=shapefile.Reader('./japan_ver84/japan_ver84.shp',encoding='SHIFT-JIS')
        SRS=src.shapeRecords()
        i = 0
        for lat_lon in self.lat_lon_arr:
            print(i)
            print(lat_lon)
            time_sta = time.time()
            LONG=float(lat_lon[1])
            LAT=float(lat_lon[0])
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
                        City.write_csv(self)
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
        cleansing.company()
        cleansing.rosen()
        cleansing.bastei_id()
        # cleansing.join()
    else:
        city = City()
        city.add_city()