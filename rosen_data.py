import pandas as pd
import re

bas_data = pd.read_csv('./乗換NEXT全データ/路線データ.csv')
# pd.set_option('display.max_rows', None)
df = pd.DataFrame(bas_data)
# df = df.rename(columns={'路線名称_x': '路線名称', 'どこからどこまで_x':'どこからどこまで', '行き方面_x':'行き方面', '帰り方面_x':'帰り方面'})
i=1
# l=1
serial_num = []
route_station = []
while ((df['路線ID']==i).sum()) != 0:
    rosen = df[df['路線ID']==i]
    rosen_meisyou = rosen['路線名称']
    houmen = re.findall(r'(.*)方面',rosen['行き方面'].iloc[0])
    from_where = re.findall(r'(.*)～',rosen['どこからどこまで'].iloc[0])
    to_where = re.findall(r'～(.*)',rosen['どこからどこまで'].iloc[0])
    # print(rosen['どこからどこまで'].iloc[0])
    # print(from_where)
    # print(to_where)
    if houmen[0] != rosen['バス停名称'].iloc[0]:
        df[df['路線ID']==i]['路線名称'].replace(rosen_meisyou+'['+rosen['バス停名称'].iloc[0]+']')
    elif rosen['バス停名称'].iloc[0] == rosen['バス停名称'].iloc[-1]:
        df[df['路線ID']==i]['路線名称'].replace(rosen_meisyou+'['+to_where[0]+']')
    else:
        df[df['路線ID']==i] = rosen.iloc[:, ::-1]
        df[df['路線ID']==i]['路線名称'].replace(rosen_meisyou+'['+rosen['バス停名称'].iloc[-1]+']')
    route_station += rosen.to_dict()
    serial_num += list(range(1, (df['路線ID']==i).sum()+1, 1))
    # l+=rosen.sum()
    i+=1
df['停車順番'] = serial_num
df = df.loc[:, ['路線順番','路線ID','バス会社ID','バス停ID','バス停名称','路線名称']]
df.to_csv('./乗換NEXT全データ/路線順番データ.csv', index_label='ID')