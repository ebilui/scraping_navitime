import pandas as pd

bas_data = pd.read_csv('./csv/query_result.csv')
# pd.set_option('display.max_rows', None)
df = pd.DataFrame(bas_data)
i=1
l=1
serial_num = []
route_station = []
while ((df['路線ID']==i).sum()) != 0:
    route_station += df[df['路線ID']==i].to_dict()
    serial_num += list(range(1, (df['路線ID']==i).sum()+1, 1))
    l+=(df['路線ID']==i).sum()
    i+=1
df['停車順番'] = serial_num
df = df.loc[:, ['路線ID', '停車順番', 'バス会社ID', 'バス停ID', 'バス停名称', '路線名称']]
df.to_csv('./csv/路線データ.csv', index=False)