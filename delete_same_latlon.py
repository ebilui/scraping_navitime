import pandas as pd
import numpy as np

bas_data = pd.read_csv('./バス停数 - シート2 (3).csv')
df = pd.DataFrame(bas_data)
df.drop_duplicates(subset=['緯度', '経度', 'バス停名称'], inplace=True)
df.index = np.arange(1, len(df)+1)
df.to_csv('./csv/乗換案内NEXTバス停一覧.csv', index_label='バス停ID')