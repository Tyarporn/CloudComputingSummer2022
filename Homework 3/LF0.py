import boto3
import random
import json
client = boto3.client('dynamodb')

def lambda_handler(event, context):
    # TODO implement

    print("event", event)
    _text = event["text"]
    _date = event["date"]
    uuid = str(int(random.randrange(432008, 1000000)))
    data = client.put_item(
        TableName='posts',
        Item={
            'uuid': {
                'S': uuid
            },
            'date': {
                'S': _date
            },
            'text': {
                'S': _text
            }
        }
    )


    return {
        'statusCode': 200,
        'TEXT': event["text"],
        'DATE': event["date"],
        'uuid': uuid,
        'body': json.dumps('Hello from Lambda!0')
    }
