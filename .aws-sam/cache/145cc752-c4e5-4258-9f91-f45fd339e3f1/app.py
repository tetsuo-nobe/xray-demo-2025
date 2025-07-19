import json
import boto3
import datetime
import os
from botocore.config import Config
from aws_xray_sdk.core import patch
patch(['boto3'])

# import requests
dynamodb = boto3.resource('dynamodb', region_name="ap-northeast-1")
sqs = boto3.client('sqs')
message = 'This is demo'

def lambda_handler(event, context):
    qurl = os.getenv('QUEUE_URL')
    table_name = os.getenv('TABLE_NAME')

    req_id = context.aws_request_id

    # キューの名前を指定してインスタンスを取得
    # queue = sqs.get_queue_by_name(QueueName=qname)
    # queue.send_message(MessageBody=message)
    response = sqs.send_message(
      QueueUrl = qurl,
      MessageBody = message
    )
    
    # DynamoDBへput_item実行
    now = str(datetime.datetime.now())
    table = dynamodb.Table(table_name)
    response = table.put_item(
       Item={
            'id': req_id,
            'message': message,
            'datetime': now
        }
    )
    #
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Done:"+ now
            # "location": ip.text.replace("\n", "")
        }),
    }
