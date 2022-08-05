Combination of s3, sns, sqs and lambda \ \

When object with extension ".tmp" is dropped in , the extension is changed into ".log". In this case "Lambda-1" is used. \


1. When object is dropped in "raw/" directory, the notification is deliverd to "SNS-1". S3 event is used. \
2. Notification about new object in raw/" directory is forwarded to "SQS-1". \
3. Message from "SQS-1" is pulled by Lambda and then processed. If file extension is ".tmp", success status is delivered to "SNS-2".
If not, failure status is delivered to "SNS-2" and message is delivered to "SQS-2". \ 
5. "SNS-2" sent notification to subscribers on mail. \
6. If "SQS-2" queue is grather than 5 messages, the CloudWatch alarm is run. \ \

Elements: \ \

Bucket does not have policy. Bucket has configured event notification with prefix "raw/" and "all object creation event" \
Event is connected to the SNS-1.
\ \ 
SNS-1 - has access policy allowing send notifation from s3 to the sns. SQS-1 is a subcriber for notification.
\ \
SQS-1 - has access policy alowing to be notified by sns.
\ \
Lambda has two scripts (for manual run and run by sqs trigger). Environmental variables must be configured. \
Lambda role has below permissions: \
-AmazonSNSFullAccess  \
-AmazonSQSFullAccess  \
-AmazonS3FullAccess  \
-AWSLambdaBasicExecutionRole
\ \
CloudWatch - alarm using "ApproximateNumberOfMessagesVisible" to minotor SQS-2




