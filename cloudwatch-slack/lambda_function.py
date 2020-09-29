

import boto3
import json
import logging
import os
import re
import sentry_sdk

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from sentry_sdk.integrations.logging import LoggingIntegration

# The base-64 encoded, encrypted key (CiphertextBlob) stored in the kmsEncryptedHookUrl environment variable
SLACK_HOOK_URL = os.environ.get('SLACK_HOOK_URL')
KMS_PREFIX = os.environ.get('KMS_PREFIX', 'base64:')
# The Slack channel to send a message to stored in the slackChannel environment variable
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL')
ENVIRONMENT = os.environ.get('ENVIRONMENT')
SENTRY_DSN = os.environ.get('SENTRY_DSN', None)

if isinstance(SLACK_HOOK_URL, (str, bytes)) and SLACK_HOOK_URL.startswith(KMS_PREFIX):
    ENCRYPTED_HOOK_URL = SLACK_HOOK_URL[len(KMS_PREFIX):]
    SLACK_HOOK_URL = boto3.client('kms') \
                          .decrypt(CiphertextBlob=b64decode(ENCRYPTED_HOOK_URL))['Plaintext'] \
                          .decode('utf-8')

LEVEL_TO_COLOR = {
    'DEBUG': '#fbe14f',
    'INFO': '#2788ce',
    'WARN': '#f18500',
    'ERROR': '#E03E2F',
    'FATAL': '#d20f2a',
}

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Sentry using the Logging Integration
sentry_logging = LoggingIntegration(
    level=logging.INFO,
    event_level=logging.ERROR
)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[sentry_logging],
)


def lambda_handler(event, context):
    message = json.loads(event['Records'][0]['Sns']['Message'])

    alarm_name = message['AlarmName']

    if re.match('^\w*\|', alarm_name) is not None:
        alarm_severity = alarm_name.split('|')[0]
    else:
        alarm_severity = alarm_name.split('-')[0]

    logger.info(f"Severity: {alarm_severity}")

    new_state = message['NewStateValue']

    if new_state == "OK":
        color = LEVEL_TO_COLOR['INFO']
    else:
        color = LEVEL_TO_COLOR.get(
                    alarm_severity,
                    'ERROR')

    alarm_description = message['AlarmDescription']
    if 'Namespace' in message['Trigger']:
        namespace = message['Trigger']['Namespace']
    else:
        namespace = message['Trigger']['Metrics'][0]['MetricStat']['Metric']['Namespace']
    if 'MetricName' in message['Trigger']:
        metric_name = message['Trigger']['MetricName']
    else:
        metric_name = message['Trigger']['Metrics'][0]['MetricStat']['Metric']['MetricName']
    reason = message['NewStateReason']

    slack_message = {
        'channel': SLACK_CHANNEL,
        'username': 'AWS CloudWatch',
        'text': 'CloudWatch Alarm - State Change',
        'attachments': [
            {
                'fallback': "%s state is now %s" % (alarm_name, new_state),
                'text': '\n'.join((
                         "*%s*" % alarm_name,
                         "*New State:* %s" % new_state,
                         "*Reason:* %s" % reason,
                         "*Description:* %s" % alarm_description,)),
                'color': color,
                'footer': "Environment: %s | Namespace: %s | Metric: %s" %
                                ( ENVIRONMENT, namespace, metric_name),
            },
        ],
    }

    req = Request(SLACK_HOOK_URL, json.dumps(slack_message).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info(f"Message posted to {SLACK_CHANNEL}" )
    except HTTPError as e:
        logger.error("Request failed: %d %s", e.code, e.reason)
    except URLError as e:
        logger.error("Server connection failed: %s", e.reason)

    return slack_message
