import json
import boto3
dynamodb = boto3.resource('dynamodb')
def lambda_handler(event, context):
    # TODO implement
    print(event)
    table = dynamodb.Table('registertable')
    scan_kwargs = {}
    response = table.scan(**scan_kwargs)
    items = response.get('Items', [])
    print(response.get('Items', []))
    return {
        'statusCode': 200,
        'headers': {
            #"Access-Control-Allow-Origin" : "*", #Required for CORS support to work
            #"Access-Control-Allow-Headers" : "authorizationtoken,application/json",
            #'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            #"Access-Control-Allow-Credentials" : True # Required for cookies, authorization headers with HTTPS 
        },
        'body': json.dumps(items)
    }
