import json
import boto3
import math

bucket = "6895-result"

def lambda_handler(event, context):
    asset_amount  = int(event['asset'])
    fapv_weight   = int(event["fapv"])
    sharpe_weight = int(event["sharpe"])
    mdd_weight    = int(event["mdd"])
    model1_filename = "model1-" + str(asset_amount) + ".json"
    model2_filename = "model2-" + str(asset_amount) + ".json"
    s3 = boto3.client("s3")
    response = s3.get_object (
        Bucket=bucket,
        Key = model1_filename   
    )
    model1 = json.loads(response['Body'].read().decode('utf-8'))
    response = s3.get_object (
        Bucket=bucket,
        Key = model2_filename   
    )
    model2 = json.loads(response['Body'].read().decode('utf-8'))
    
    # choose from two models 
    # fapv, sharpe higher is better; mdd lower is better
    score1 = 0
    score2 = 0
    if float(model1['fapv']) >= float(model2['fapv']):
        score1 += fapv_weight
    else:
        score2 += fapv_weight
    if float(model1['sharpe']) >= float(model2['sharpe']):
        score1 += sharpe_weight
    else:
        score2 += sharpe_weight
    if float(model1['mdd'] >= float(model2['mdd'])):
        score2 += mdd_weight
    else:
        score1 += mdd_weight
    if score1 >= score2:
        choosen_model = model1
    else:
        choosen_model = model2
    weight_vector = choosen_model['weight_vector']
    
    # choose 5 assets
    asset_indexes = []
    for i in range(len(weight_vector)):
        asset_indexes.append([i, weight_vector[i]])
    selected_indexes = sorted(asset_indexes, key = lambda x:float(x[1]), reverse=True)
    selected_indexes = selected_indexes[:6]
    
    if choosen_model == model1:
        map_key = "model1_mapping.json"
    else:
        map_key = "model2_mapping.json"
    
    response = s3.get_object (
        Bucket = bucket,
        Key = map_key
    )
    mapping = response['Body'].read().decode('utf-8')
    mapping = json.loads(mapping)
    count = 0
    asset_set = []
    cash = asset_amount
    for i in range(len(selected_indexes)):
        if count >= 5:
            break
        if selected_indexes[i][0] == 0:
            continue
        asset_name = mapping[selected_indexes[i][0]]['name']
        asset_price = mapping[selected_indexes[i][0]]['price']
        asset_share= math.floor(asset_amount * float(selected_indexes[i][1]) / asset_price)
        asset_info = [asset_name, asset_share, asset_price * asset_share]
        cash -= asset_info[2]
        asset_set.append(asset_info)
        print("Buy asset " + asset_name + " " + str(asset_share))
        count += 1
    result = {}
    print(cash)
    result = {}
    result['cash'] = cash
    for i in range(len(asset_set)):
        key = 'comp' + str(i + 1)
        item = asset_set[i]
        if item[1] != 0:
            result[key] = item
    response = {"isBase64Encoded": False,
    "statusCode": 200,
    "headers": {"Access-Control-Allow-Origin":"*"},
    "body":result}
    return response
