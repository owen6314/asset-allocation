import pandas as pd
from datetime import datetime
import time
import os
import sqlite3

db_path = "test.db"
conn = sqlite3.connect(db_path)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

root_dir = 'sample/'
new_dir = 'new_sample/'
for file in os.listdir(root_dir):
    if '.csv' in file:
        df = pd.read_csv(root_dir + file)
        df = df[['Date', 'Name', 'High', 'Low', 'Open', 'Close', 'Volume']]
        print(df)
        f = lambda x: time.mktime(datetime.strptime(x, "%Y-%m-%d").timetuple())
        df['Date'] = df['Date'].apply(f)
        df = df.astype({'Date': 'int'})
        print(df)
        break
        # df.to_sql('history', conn, if_exists='append', index=False)
        # df.to_csv(new_dir + file[:-4] + "_new.csv", index=False)
