import pandas as pd
import os
from datetime import datetime
import time

root_dir = 'sample/'
result_file = 'all.csv'
counter = 0

result_df = pd.DataFrame(columns=['DateTime'])

if not os.path.exists(root_dir):
    os.mkdir(root_dir)

for file in os.listdir(root_dir):
    if '.csv' in file:
        print("processing: " + file)
        stock_name = file[:-4]
        df = pd.read_csv(root_dir + file)
        df = df[['Date', 'Close']]
        if len(df) < 1258:
            continue
        if len(result_df) == 0:
            result_df['DateTime'] = df['Date']
            f = lambda x: datetime.strptime(x, "%Y-%m-%d").strftime('%Y%m%d')
            result_df['DateTime'] = result_df['DateTime'].apply(f)
        result_df[stock_name] = df['Close']
        counter += 1

print("Total file number: " + str(counter))
result_df.to_csv(result_file, index=False)

