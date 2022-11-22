import pandas as pd

def a():
    df = pd.read_csv('./csv/バス路線.csv')
    df2 = pd.read_csv('./csv/路線データ.csv')
    df2 = df2.drop(['バス会社ID','バス停ID'], axis=1)
    df_merged = pd.merge(df, df2, on=['バス停名称', '路線名称'])
    df_s = df_merged.sort_values('ID')
    df_s.to_csv('./csv/rosen_junban.csv', index=False)

    df = pd.read_csv('./csv/rosen_junban.csv', encoding='utf-8')
    df2 = pd.read_csv('./csv/パートさんA - シート3.csv', encoding='utf-8')

    # universitiesのIDを学校IDという名前に変更する
    # df2_ = df2.rename(columns={'ID': '学校ID'})

    # 学校IDというキーを元にして２つのCSVを結合する
    df_merged = pd.merge(df, df2, on=['緯度','経度'])
    df_s = df_merged.sort_values('ID')
    df_s = df_s.loc[:, ['ID', 'バス会社名称', '路線ID', '停車順番', 'バス停名称', '路線名称', '緯度', '経度', '市区町村名']]
    df_s.to_csv("./csv/kunai_data.csv", index=False)

def b():
    city = ['葛飾区', '文京区', '江戸川区', '港区', '江東区', '荒川区', '渋谷区', '新宿区', '杉並区', '世田谷区', '千代田区', '足立区', '台東区', '大田区', '中央区', '中野区', '板橋区', '品川区', '豊島区', '北区', '墨田区', '目黒区', '練馬区']
    df = pd.read_csv('./バス停数 - バス停市区町村 (1).csv')
    df2 = pd.read_csv('./csv/.csv')
    df_merged = pd.concat([df, df2], axis=1, join='inner')
    df_s = df_merged.sort_values('バス停ID')
    df_s = df_s[df_s['市区町村名'].isin(city)]
    # print(df_merged)
    serial_num = pd.RangeIndex(start=1, stop=len(df_s.index) + 1, step=1)
    df_s['区内バス停ID'] = serial_num
    df_s = df_s.loc[:, ['市区町村名', '緯度', '経度', '区内バス停ID', '会社名称','路線名称','どこからどこまで','行き方面','帰り方面','バス停名称','url','同じバス停']]
    df_s.to_csv('./csv/乗換案内NEXT区内バス停.csv', index=False)

def c():
    pd.set_option('display.max_columns', 60)
    df = pd.read_csv('./csv/乗換案内NEXT区内バス停.csv')
    df2 = pd.read_csv('./csv/乗換案内NEXT路線.csv')
    df["緯度"] = df["緯度"].astype(str)
    df["経度"] = df["経度"].astype(str)
    df2["緯度"] = df2["緯度"].astype(str)
    df2["経度"] = df2["経度"].astype(str)
    df_merged = pd.merge(df, df2, how='inner', on=['緯度', '経度', 'バス停名称'])
    print(df_merged)
    df_s = df_merged.sort_values('路線一覧ID')
    df_s = df_s.loc[:, ['路線一覧ID','会社名称_x','路線名称_x','どこからどこまで_x','行き方面_x','帰り方面_x','区内バス停ID','市区町村名','バス停名称','url_x','緯度','経度','同じバス停_x']]
    df_s.to_csv('./csv/乗換案内NEXT区内路線.csv', index=False)
    # ID,路線ID,停車順番,路線名称,元バス停名称,,変更後バス停名称,緯度,経度,URL,,,,,,,"https://www.google.co.jp/maps/place/35%C2%B042'41.2%22N+139%C2%B046'31.2%22E/@35.70699,139.772551,21z/data=!4m5!3m4!1s0x0:0xa391560fdb724a45!8m2!3d35.70699!4d139.772551?hl=ja"

def d():
    city = ['error']
    df = pd.read_csv('./バス停数 - バス停市区町村 (1).csv')
    df2 = pd.read_csv('./csv/乗換案内NEXTバス停一覧.csv')
    df_merged = pd.concat([df, df2], axis=1, join='inner')
    df_s = df_merged.sort_values('バス停ID')
    df_s = df_s[df_s['市区町村名'].isin(city)]
    # print(df_merged)
    serial_num = pd.RangeIndex(start=1, stop=len(df_s.index) + 1, step=1)
    df_s['区内バス停ID'] = serial_num
    df_s = df_s.loc[:, ['市区町村名', '緯度', '経度', '区内バス停ID', '会社名称','路線名称','どこからどこまで','行き方面','帰り方面','バス停名称','url','同じバス停']]
    df_s.to_csv('./csv/乗換案内NEXTerrorバス停.csv', index=False)

def e():
    df = pd.read_csv('./バス停数 - シート2 (3).csv')
    df.to_csv('./csv/乗換案内NEXT路線.csv', index_label='路線一覧ID')

c()