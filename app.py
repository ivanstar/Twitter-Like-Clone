from decimal import Decimal
from flask import Flask, jsonify, request, g, Response
import boto3
from boto3.dynamodb.conditions import Key
import create_table
import json
import uuid
import datetime
import requests

app = Flask(__name__)

dynamo_client = boto3.client('dynamodb',endpoint_url="http://localhost:8000")
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
endpoint = "http://localhost:8000"

def load_table(dm,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('directmsg_user')
    
    for users in dm:
        user = users['username']
        msgId = users['fromUser']
        table.put_item(Item=users)




@app.cli.command('init')
def init_db():
    create_table.directmsg()
    with open("test-load.json") as json_file:
        msg_list = json.load(json_file, parse_float=Decimal)
    load_table(msg_list)
        

@app.route('/')
def index():
    return "This is the main page."

@app.route('/listmsg/<username>',methods=['GET'])
def listDirectMessageFor(username,dynamodb=None):    
    
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint)

    table = dynamodb.Table('directmsg_user')
    
    response = table.query( KeyConditionExpression=Key('username').eq(username))

    text = response['Items'][0]['username']
    text1 = response['Items'][0]['textmsg']
    return jsonify(f"Username: {text}  Textmessage: {text1}"), 200
    
@app.route('/listreplies/<txtid>',methods=['GET'])
def listRepliesTo(txtid,dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint)
    
    table = dynamodb.Table('directmsg_user')


    response = table.query(
            IndexName='text_index',
            KeyConditionExpression=Key('textID').eq(txtid))

    userid = response['Items'][0]['textID']
    text1 = response['Items'][0]['textmsg']
    return jsonify(f"Text ID: {userid} TextMessage: {text1}"), 200
    


@app.route('/print-items')
def get_items():
    dynamo_scan = dynamo_client.scan(TableName='directmsg_user')
    return jsonify(dynamo_scan)

@app.route('/sendmsg',methods=['POST'])
def sendDirectMessage(dynamodb=None):

    queryInfo = request.get_json()
    
    to = queryInfo.get('to')
    msgFrom = queryInfo.get('from')
    msg = queryInfo.get('message')

    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint)
    

    table = dynamodb.Table('directmsg_user')
    textId = uuid.uuid4().hex

    response = table.put_item(
            Item={
                'textID' : textId,
                'username' : to,
                'fromUser': msgFrom,
                'textmsg' : msg,
                'timestamp' : datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            }
    )
    return response
    
@app.route('/replyto',methods=['POST'])
def replyToDirectMessage(dynamodb=None):
    
    queryInfo = request.get_json()

    to = queryInfo.get('to')
    msgFrom = queryInfo.get('from')
    msg = queryInfo.get('message')
    quick_reply = queryInfo.get('quick-reply')
    reply_to_id = queryInfo.get('reply-to-id')
    #app.logger.debug(quick_reply)
    
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint)
    
    table = dynamodb.Table('directmsg_user')
    textId = uuid.uuid4().hex
    
    resp = table.query( KeyConditionExpression=Key('username').eq(to))
    
    if 'quick-reply' in queryInfo:
        msg = resp['Items'][0]['quick-replies'][int(quick_reply)]

    response = table.put_item(
            Item={
                'textID' : textId,
                'username' : to,
                'fromUser': msgFrom,
                'textmsg' : msg,
                'reply-to-id' : reply_to_id,    #Text ID from the on-going message
                'timestamp' : datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
            }
    )
    return response




#if __name__ == '__main__':
#    app.run()
