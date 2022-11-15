import pandas as pd
import mojimoji

df = pd.read_csv('./csv/バス停数.csv')
df2 = pd.read_csv('./csv/kunai_data.csv')

df2 = df2.replace('\(.+?\)', {'バス停名称':''}, regex=True)
df['バス停名称'] = df['バス停名称'].apply(mojimoji.zen_to_han, kana=False)
counts = df2.pivot_table(index=['バス停名称'], aggfunc='size')
# print(df2)
# print(counts.loc['IHI前'])
# print(counts.loc['2号バース前'])
print(df2[df2['バス停名称']=='いかづち公園前'])
# print(df2[df2['バス停名称']=='上野松坂屋前'].values.tolist()[0])
for name in df['バス停名称']:
    gachi_name = df[df['バス停名称']==name]['バス停数'].to_list()[0]
    moto_name = counts.loc[name]
    moto_name = moto_name.tolist()
    # print(gachi_name)
    if gachi_name == 'None':
        continue
    if int(gachi_name) > moto_name:
        value = df2[df2['バス停名称']==name].values.tolist()[0]
        # print(value)
        df2.loc[len(df2), df2.columns] = value
# print(df2.pivot_table(index=['バス停名称'], aggfunc='size').loc['いかづち公園前'])
# print(df2[df2['バス停名称']=='いかづち公園前'])
df2.sort_values(by='バス停名称', inplace=True)
df2.to_csv('./csv/正しいバス停数.csv')