import json
import base64
import re
import reg_crypto
import boto3

dynamodb = boto3.resource('dynamodb')
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def lambda_handler(event, context):
    # TODO implement
    print((event['body']))
   
    data = json.loads(base64.b64decode(event['body']))
    username = data["username"]
    email = data["email"]
    pw1 = data["password1"]
    pw2 = data["password2"]
    if len(username) == 0 or len(pw1) == 0 or len(email)==0:
        return {
            'statusCode': 201,
            'body': json.dumps("Email, username or password must not be empty")
        }
    if (pw1 != pw2):
        return {
            'statusCode': 201,
            'body': json.dumps("Password must be same!")
        }
    if (not re.search(regex,email)):
        return {
            'statusCode': 201,
            'body': json.dumps("Email format is wrong")
        }
    sig = reg_crypto.signregister(email,username,pw1)
    table = dynamodb.Table('registertable')
    response = table.put_item(
       Item={
            'email': email,
            'username': username,
            'password': pw1,
            'signature': sig
        }
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(sig)
    }
