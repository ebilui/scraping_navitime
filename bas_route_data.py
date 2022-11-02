import pandas as pd
bas_data = pd.read_csv('./バス路線.csv')
df = pd.DataFrame(bas_data)
print(df.duplicated(subset=['路線名']).sum())
df.drop_duplicates(subset=['路線名'], inplace=True)
df.to_csv('./路線.csv', index=False)