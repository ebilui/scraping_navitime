import pandas as pd
bas_data = pd.read_csv('./バス路線.csv')
df = pd.DataFrame(bas_data)
df.sort_values(by='バス停名', inplace=True)
print(df.duplicated(subset=['緯度', '経度']).sum())
df.drop_duplicates(subset=['緯度', '経度'], inplace=True)
df.to_csv('./バス停.csv', index=False)