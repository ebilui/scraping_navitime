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
    df = pd.read_csv('./csv/パートさんA - シート3.csv')
    df2 = pd.read_csv('./csv/ver.2バス停.csv')
    df_merged = pd.merge(df, df2, on=['緯度', '経度'])
    df_s = df_merged.sort_values('バス停ID')
    serial_num = pd.RangeIndex(start=1, stop=len(df_s.index) + 1, step=1)
    df_s['区内バス停ID'] = serial_num
    df_s = df_s.loc[:, ['市区町村名', '緯度', '経度', '区内バス停ID', 'バス会社名称', 'バス停名称']]
    df_s.to_csv('./csv/区内バス停.csv', index=False)

def c():
    df = pd.read_csv('./パートさんA - シート4.csv')
    df2 = pd.read_csv('./2022_11_11 - 路線.csv')
    df_merged = pd.merge(df, df2, on=['緯度', '経度'])
    df_s = df_merged.sort_values('ID')
    df_s = df_s.loc[:, ['ID', '路線ID', '停車順番', '路線名称', '元バス停名称', '1', '変更後バス停名称', '緯度', '経度', 'URL', '市区町村名', '2', '3', '4', '5', '6', '7', "https://www.google.co.jp/maps/place/35%C2%B042'41.2%22N+139%C2%B046'31.2%22E/@35.70699,139.772551,21z/data=!4m5!3m4!1s0x0:0xa391560fdb724a45!8m2!3d35.70699!4d139.772551?hl=ja"]]
    df_s.to_csv('./output.csv', index=False)
    # ID,路線ID,停車順番,路線名称,元バス停名称,,変更後バス停名称,緯度,経度,URL,,,,,,,"https://www.google.co.jp/maps/place/35%C2%B042'41.2%22N+139%C2%B046'31.2%22E/@35.70699,139.772551,21z/data=!4m5!3m4!1s0x0:0xa391560fdb724a45!8m2!3d35.70699!4d139.772551?hl=ja"
c()