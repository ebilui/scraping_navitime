import pandas as pd

bas_data = pd.read_csv('./１バス停navitime.csv')
df = pd.DataFrame(bas_data)
list = df['変更後バス停名称'].to_list()
bas_data = pd.read_csv('./csv/乗換案内NEXT区内バス停.csv')
df2 = pd.DataFrame(bas_data)
target = df2.index[(df2['バス停名称'] in list)]
print(target)