import json
import boto3
import os 

def lambda_handler(event, context):
    sqs_2_url = os.environ['sqs_2_url']
    sns_arn_topic = os.environ['sns_arn_topic']

    sqs_client = boto3.client('sqs')
    sns_client = boto3.client('sns')
    s3c = boto3.client('s3')
    s3r = boto3.resource('s3')
    
    body = json.loads(event['Records'][0]['body'])   
    message = json.loads(body['Message'])
    s3 = (message['Records'][0]['s3'])
    bucket_name = s3['bucket']['name']
    file_name = (s3['object']['key'])
    suffix = file_name.split('.')[1]
    print(file_name)

    if suffix == 'tmp':
        file_data = {
            'Bucket': bucket_name,
            'Key': file_name
        }
        new_extension = file_name.split('.')[0]+'.log'
        new_path = new_extension.replace('raw/', 'processed/', 1)
        s3r.meta.client.copy(file_data, bucket_name, new_path)
        s3c.delete_object(Bucket = bucket_name, Key = file_name)
        response = sns_client.publish(
            TopicArn = sns_arn_topic,
            Message = json.dumps({
                'status': 'success',
                'file name': file_name
            })
        ) 
        
    else:
        response = sns_client.publish(
            TopicArn = sns_arn_topic,
            Message = json.dumps({
                'status': 'failed',
                'file name': file_name
            })
        ) 
            
        response = sqs_client.send_message(
            QueueUrl = sqs_2_url,
            MessageBody = json.dumps({
                'new file': file_name,
                'extension': suffix
            })                
        )