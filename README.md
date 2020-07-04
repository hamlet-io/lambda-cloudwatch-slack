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
npm install
npx sls invoke local -f cloudwatch-slack --path cloudwatch-slack/events/event.json --docker
```

## Packaging

To create a zip package for lambda deployment

```bash
npx sls package
```

This will create the lambda.zip and place it `.serverless/<function name>.zip`

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
