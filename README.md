# Cloud Watch Alarm to Slack

Provides a way to send CloudWatch Alarm State changes through to slack

## Configuration

Environment Variables

* SLACK_HOOK_URL - The incoming webhook slack URL
* KMS_PREFIX - The prefix applied to environment variables which are encrypted using KMS
* SLACK_CHANNEL - The slack channel name to send the message to
* ENVIRONMENT - The name of the environment the message came from

## Testing

You can run the script locally using the lambda-local-run python package ( included in requirements )

```bash
# from cloudwatch_slack dir

export <Configuration Environment Variables>
python-lambda-local -f lambda_handler src/lambda_function.py src/event.json
```

Which shows the lambda log style output

```text
root - INFO - 2019-11-20 22:55:11,035] Event: {'Records': [{'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:ap-southeast-2:123456789012:sns-lambda:21be56ed-a058-49f5-8c98-aedd2564c486', 'EventSource': 'aws:sns', 'Sns': {'SignatureVersion': '1', 'Timestamp': '2019-01-02T12:45:07.000Z', 'Signature': 'tcc6faL2yUC6dgZdmrwh1Y4cGa/ebXEkAi6RibDsvpi+tE/1+82j...65r==', 'SigningCertUrl': 'https://sns.us-east-2.amazonaws.com/SimpleNotificationService-ac565b8b1a6c5d002d285f9598aa1d9b.pem', 'MessageId': '95df01b4-ee98-5cb9-9903-4c221d41eb5e', 'Subject': 'ALARM: "DEBUG-api-production-api-backend-5XXLBResponse" in ap-southeast-2', 'Message': '{"AlarmName":"DEBUG-api-production-api-backend-5XXLBResponse","AlarmDescription":"Example alarm description.","AWSAccountId":"123456789012","NewStateValue":"ALARM","NewStateReason":"Threshold Crossed: 1 datapoint (10.0) was greater than or equal to the threshold (1.0).","StateChangeTime":"2019-01-02T12:45:07.000Z","Region":"ap-southeast-2","OldStateValue":"OK","Trigger":{"MetricName":"5XXResponse","Namespace":"APIGateway","Statistic":"SUM","Unit":null,"Dimensions":[],"Period":300,"EvaluationPeriods":1,"ComparisonOperator":"GreaterThanOrEqualToThreshold","Threshold":1.0}}', 'MessageAttributes': {'Test': {'Type': 'String', 'Value': 'TestString'}, 'TestBinary': {'Type': 'Binary', 'Value': 'TestBinary'}}, 'Type': 'Notification', 'UnsubscribeUrl': 'https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&amp;SubscriptionArn=arn:aws:sns:us-east-2:123456789012:test-lambda:21be56ed-a058-49f5-8c98-aedd2564c486', 'TopicArn': 'arn:aws:sns:us-east-2:123456789012:sns-lambda'}}]}
[root - INFO - 2019-11-20 22:55:11,035] START RequestId: 21721db4-84e4-4ac7-85f2-22bd76719c3f Version:
[root - INFO - 2019-11-20 22:55:11,043] Event: {'Records': [{'EventVersion': '1.0', 'EventSubscriptionArn': 'arn:aws:sns:ap-southeast-2:123456789012:sns-lambda:21be56ed-a058-49f5-8c98-aedd2564c486', 'EventSource': 'aws:sns', 'Sns': {'SignatureVersion': '1', 'Timestamp': '2019-01-02T12:45:07.000Z', 'Signature': 'tcc6faL2yUC6dgZdmrwh1Y4cGa/ebXEkAi6RibDsvpi+tE/1+82j...65r==', 'SigningCertUrl': 'https://sns.us-east-2.amazonaws.com/SimpleNotificationService-ac565b8b1a6c5d002d285f9598aa1d9b.pem', 'MessageId': '95df01b4-ee98-5cb9-9903-4c221d41eb5e', 'Subject': 'ALARM: "DEBUG-api-production-api-backend-5XXLBResponse" in ap-southeast-2', 'Message': '{"AlarmName":"DEBUG-api-production-api-backend-5XXLBResponse","AlarmDescription":"Example alarm description.","AWSAccountId":"123456789012","NewStateValue":"ALARM","NewStateReason":"Threshold Crossed: 1 datapoint (10.0) was greater than or equal to the threshold (1.0).","StateChangeTime":"2019-01-02T12:45:07.000Z","Region":"ap-southeast-2","OldStateValue":"OK","Trigger":{"MetricName":"5XXResponse","Namespace":"APIGateway","Statistic":"SUM","Unit":null,"Dimensions":[],"Period":300,"EvaluationPeriods":1,"ComparisonOperator":"GreaterThanOrEqualToThreshold","Threshold":1.0}}', 'MessageAttributes': {'Test': {'Type': 'String', 'Value': 'TestString'}, 'TestBinary': {'Type': 'Binary', 'Value': 'TestBinary'}}, 'Type': 'Notification', 'UnsubscribeUrl': 'https://sns.us-east-2.amazonaws.com/?Action=Unsubscribe&amp;SubscriptionArn=arn:aws:sns:us-east-2:123456789012:test-lambda:21be56ed-a058-49f5-8c98-aedd2564c486', 'TopicArn': 'arn:aws:sns:us-east-2:123456789012:sns-lambda'}}]}
[root - INFO - 2019-11-20 22:55:11,049] Message: {'AlarmName': 'DEBUG-api-production-api-backend-5XXLBResponse', 'AlarmDescription': 'Example alarm description.', 'AWSAccountId': '123456789012', 'NewStateValue': 'ALARM', 'NewStateReason': 'Threshold Crossed: 1 datapoint (10.0) was greater than or equal to the threshold (1.0).', 'StateChangeTime': '2019-01-02T12:45:07.000Z', 'Region': 'ap-southeast-2', 'OldStateValue': 'OK', 'Trigger': {'MetricName': '5XXResponse', 'Namespace': 'APIGateway', 'Statistic': 'SUM', 'Unit': None, 'Dimensions': [], 'Period': 300, 'EvaluationPeriods': 1, 'ComparisonOperator': 'GreaterThanOrEqualToThreshold', 'Threshold': 1.0}}
[root - INFO - 2019-11-20 22:55:11,446] Message posted to #codepublican-integration
[root - INFO - 2019-11-20 22:55:11,452] END RequestId: 21721db4-84e4-4ac7-85f2-22bd76719c3f
[root - INFO - 2019-11-20 22:55:11,452] REPORT RequestId: 21721db4-84e4-4ac7-85f2-22bd76719c3f  Duration: 405.34 ms
[root - INFO - 2019-11-20 22:55:11,452] RESULT:
```

## Setting up the Slack incoming Webhook

Follow these steps to configure the webhook in Slack:

  1. Navigate to https://<your-team-domain>.slack.com/services/new

  2. Search for and select "Incoming WebHooks".

  3. Choose the default channel where messages will be sent and click "Add Incoming WebHooks Integration".

  4. Copy the webhook URL from the setup instructions and use it in the next section.

## Slack Webhook Encryption

Since slack webhook URLS contain a secret key to send messages to slack its a good idea to encrypt them using KMS so that you can pass them via an environment Variable

Encrypt the webhook url using KMS ( via the manageCrypto command in [CodeOnTap](https://codeontap.io/) ), and append the kms prefix ( default `base64:` ) to the returned base64 encoded string

### KMS IAM Permissions Required

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Stmt1443036478000",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": [
                "<your KMS key ARN>"
            ]
        }
    ]
}
```
