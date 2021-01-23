import os
import json

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    
    translate = boto3.client(service_name='translate', region_name='us-east-1', use_ssl=True)
    
    
    print('Texto del item: ')
    print(result['Item']['text'])
    
    
    translatedText = translate.translate_text(Text=result['Item']['text'], 
            SourceLanguageCode="auto", TargetLanguageCode=event['pathParameters']['language'])
            
    result['Item']['text'] = translatedText['TranslatedText']
    
    print('Texto del item: ')
    print(result['Item']['text'])
   
   
   # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }


    return response
