import pandas as pd


df = pd.DataFrame(columns=['index', 'name', 'price'])
# model1 processing
'''
with open('model1_vector.txt', 'r') as f:
    names = f.read()
    names = names.replace("'", '')
    names = names.strip('[]').split(', ')
    for i in range(len(names)):
        asset_name = names[i]
        asset_file = 'sample/' + asset_name + "_data.csv"
        temp_df = pd.read_csv(asset_file)
        price = float(temp_df.iloc[-1]['Close'])
        df = df.append({'index': i, 'name': asset_name, 'price': price}, ignore_index=True)
    print(df)
    df.to_csv('model1_mapping.csv', index=False)
'''
# model2 processing
with open('model2_vector.txt', 'r') as f:
    names = f.read()
    names = names.split(',')
    for i in range(len(names)):
        asset_name = names[i][:-5]
        asset_file = 'sample/' + asset_name + "_data.csv"
        temp_df = pd.read_csv(asset_file)
        price = float(temp_df.iloc[-1]['Close'])
        df = df.append({'index': i, 'name': asset_name, 'price': price}, ignore_index=True)
    print(df)
    df.to_csv('model2_mapping.csv', index=False)

