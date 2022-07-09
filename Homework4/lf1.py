import json
import boto3
import urllib3
from boto3.dynamodb.conditions import Key
client = boto3.client('sns')
bot = boto3.client('lexv2-runtime')
snsArn = 'arn:aws:sns:us-east-1:004807650303:postsearcher'


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    # TODO implement

    endpoint = 'https://search-posts-q7u3gw4633m6tmnvr73q6hw4yu.us-east-1.es.amazonaws.com'
    headers = { "Content-Type": "application/json" }
    content_string = ""
    message = ""

    query = event['params']['querystring']['q']
    http = urllib3.PoolManager()
    response = bot.recognize_text(
        botId='FF1EJQCSJW',
        botAliasId='TSTALIASID',
        localeId='en_US',
        sessionId="test_session",
        text=query
        )

    print(response['sessionState']['intent']['slots']['tag']['values'])
    values = response['sessionState']['intent']['slots']['tag']['values']
    tags = []
    for v in values:
        val = v['value']['interpretedValue']
        print(val)
        tags.append(val)

    index = "posts"
    # try:
    #     tags = [event['params']['querystring']['q']] # change for assignment 3
    # except:
    #     tag_raw = event['currentIntent']['slots']['tags'] # assignment 4
    #     tags = tag_raw.split(" and ")

    # print(tags)
    # print(event)
    for t in tags:
        header = urllib3.make_headers(basic_auth='ta1693:Qwerty1234!')

        url = endpoint + '/' + index + '/_search' + '?q=' + t

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

    # print(ids)

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
        content_string += (' '+ t)

        message += (t + "\n\n")
        for p in posts:
            message += (p + "\n\n")


    response = client.publish(
    TopicArn = snsArn,
    Message = message ,
    Subject='Your Lex response for ' + content_string + '!'
    )


    return {
        'statusCode': 200,
        'posts': posts,
        'message': message,
        'body': json.dumps('Hello from Lambda!10')
        }
