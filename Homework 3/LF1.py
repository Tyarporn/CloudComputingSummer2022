import json
import boto3
import urllib3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')



def lambda_handler(event, context):
    # TODO implement

    endpoint = 'https://search-posts-q7u3gw4633m6tmnvr73q6hw4yu.us-east-1.es.amazonaws.com'
    headers = { "Content-Type": "application/json" }


    http = urllib3.PoolManager()

    index = "posts"
    tag = event['params']['querystring']['q']
    header = urllib3.make_headers(basic_auth='ta1693:Qwerty1234!')

    url = endpoint + '/' + index + '/_search' + '?q=' + tag

    result = http.request('GET', url,headers = header)
    print(json.loads(result.data))
    print(result.status)

    data = json.loads(result.data)

    ids = []
    for i in range(3):
        try:
            id = data['hits']['hits'][i]['_source']['id']
            ids.append(id)
        except:
            break

    print(ids)

    posts = []
    for pid in ids:
        table = dynamodb.Table('posts')
        resp = table.query(KeyConditionExpression=Key('uuid').eq(pid))
    # print(resp)
        print(resp['Items'][0][' posts'])
        posts.append(resp['Items'][0][' posts'])

    if(len(posts) == 0):
        posts.append("No Post Found!")
        posts.append("--")
        posts.append("--")
    elif(len(posts) == 1):
        posts.append("--")
        posts.append("--")
    elif(len(posts) == 1):
        posts.append("--")


    print("event", event)
    print("context", context)
    return {
        'statusCode': 200,
        'query': event['params']['querystring']['q'],
        'posts': posts,
        'body': json.dumps('Hello from Lambda!10')
    }
