import json
import boto3
import os

def lambda_handler(event, context):
    sqs_1_url = os.environ['sqs_1_url']
    sqs_2_url = os.environ['sqs_2_url']
    sns_arn_topic = os.environ['sns_arn_topic']

    sqs_client = boto3.client('sqs')
    sns_client = boto3.client('sns')
    s3c = boto3.client('s3')
    s3r = boto3.resource('s3')

    messages = sqs_client.receive_message(
        QueueUrl = sqs_1_url, 
        MaxNumberOfMessages = 10,
        WaitTimeSeconds = 20,
        MessageAttributeNames = ['All']
        )
        
    if not 'Messages' in messages:
        return 'New file not found'
    else:    
        receipthandle=messages['Messages'][0]['ReceiptHandle']    
        for m in messages['Messages']:
            body = json.loads(m['Body'])
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
        sqs_client.delete_message(QueueUrl=sqs_1_url, ReceiptHandle=receipthandle)


  
