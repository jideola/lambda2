import json
import requests
import boto3
from botocore.exceptions import ClientError


def get_secret():

    secret_name = "slack-token"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        print(f"Failed to acquired {secret_name}")
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    tsecret = json.loads(secret)
    print(f"Successfully acquired {secret_name} from secretsmanager")
    return tsecret["slack-token"]


##############################################


def lambda_handler(event, context):
    # Slack API endpoint
    url = "https://slack.com/api/chat.postMessage"

    # Slack API token (needs "chat:write" scope)
    token = get_secret()
    alarm = json.loads(event['Records'][0]['Sns']["Message"])

    if alarm["NewStateValue"] != "OK":
        color = "#ff0000"
    else:
        color = "#36a64f"
    # Slack message payload
    message = {
        "channel": "guardian",
        "attachments": [
            {
    	        "mrkdwn_in": ["text"],
                "color": color,
                "title": alarm["AlarmName"],
                "fields": [
                    {
                        "title": "Alarm Description",
                        "value": alarm["AlarmDescription"],
                        "short": False
                    },
                    {
                        "title": "Alarm Region",
                        "value": alarm["Region"],
                        "short": False
                    },
                    {
                        "title": "Previous state",
                        "value": alarm["OldStateValue"],
                        "short": True
                    },
                    {
                        "title": "Current State",
                        "value": alarm["NewStateValue"],
                        "short": True
                    }
                ],
                "thumb_url": "http://placekitten.com/g/200/200",
                "footer": "footer",
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"
            }
        ]
    }

    # Set headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    # Make request to Slack API
    response = requests.post(url, headers=headers, data=json.dumps(message))
    json_message = json.dumps(message)
    print(json_message)
    #######################################
    a = response.json()
    print("Return message from slack.")
    print(json.dumps(a))
    #######################################
    return {
        'statusCode': 200,
        'body': response.json()
    }

event={
  "Records": [
    {
      "EventSource": "aws:sns",
      "EventVersion": "1.0",
      "EventSubscriptionArn": "arn:aws:sns:us-east-1:951708231033:guardian:915d1719-b414-4500-a15d-960ff6a8f6e7",
      "Sns": {
        "Type": "Notification",
        "MessageId": "c0a141f9-6478-51b7-a33e-1d926611b692",
        "TopicArn": "arn:aws:sns:us-east-1:951708231033:guardian",
        "Subject": "OK: \"api-jideola domain alarm\" in US East (N. Virginia)",
        "Message": "{\"AlarmName\":\"api-jideola domain alarm\",\"AlarmDescription\":\"This metric checks the status of the api-jideola.com health check.\",\"AWSAccountId\":\"951708231033\",\"AlarmConfigurationUpdatedTimestamp\":\"2023-02-18T16:41:38.351+0000\",\"NewStateValue\":\"OK\",\"NewStateReason\":\"Threshold Crossed: 2 out of the last 2 datapoints [3.0 (18/02/23 16:42:00), 3.0 (18/02/23 16:41:00)] were not less than the threshold (1.0) (minimum 1 datapoint for ALARM -> OK transition).\",\"StateChangeTime\":\"2023-02-18T16:43:21.231+0000\",\"Region\":\"US East (N. Virginia)\",\"AlarmArn\":\"arn:aws:cloudwatch:us-east-1:951708231033:alarm:api-jideola domain alarm\",\"OldStateValue\":\"ALARM\",\"OKActions\":[\"arn:aws:sns:us-east-1:951708231033:guardian\"],\"AlarmActions\":[\"arn:aws:sns:us-east-1:951708231033:guardian\"],\"InsufficientDataActions\":[\"arn:aws:sns:us-east-1:951708231033:guardian\"],\"Trigger\":{\"MetricName\":\"HealthCheckStatus\",\"Namespace\":\"AWS/Route53\",\"StatisticType\":\"Statistic\",\"Statistic\":\"SAMPLE_COUNT\",\"Unit\":null,\"Dimensions\":[{\"value\":\"afdf0e5a-b5ec-4eb0-8140-4fb83e928df6\",\"name\":\"HealthCheckId\"}],\"Period\":60,\"EvaluationPeriods\":2,\"DatapointsToAlarm\":2,\"ComparisonOperator\":\"LessThanThreshold\",\"Threshold\":1.0,\"TreatMissingData\":\"breaching\",\"EvaluateLowSampleCountPercentile\":\"\"}}",
        "Timestamp": "2023-02-18T16:43:21.290Z",
        "SignatureVersion": "1",
        "Signature": "ii0riQwVcEMJ5EK+yhZzDeXVKwAugACj0sUfMwMIVdqbQumHtrzqv6SiefVuVeKc805UDzsvkh6B5AaKeZS/fs/sa4dax1r6NfK7BeVxOhO0gwFxPVLp+eMZk/5qRzA2/bCU0sOnYHHClOel1D08jU5DodaDn0Fq6eLKCMgbTlk1TwXC+NsGwo/bgI5eiGg96iahmeJOlPNy0h/5YR6RVcdKiPz92DYoUmY6zMAJLxI3IBdDvv/TSju4KHnFTIVIh40Yl3r4IN7C2X2eBBC+jhKWBxM8uW+QTRFDckKyghFwksmX5y+Tgrfd4Je8wosWVs8ZpScedZaqsCje3oBrbA==",
        "SigningCertUrl": "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-56e67fcb41f6fec09b0196692625d385.pem",
        "UnsubscribeUrl": "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:951708231033:guardian:915d1719-b414-4500-a15d-960ff6a8f6e7",
        "MessageAttributes": {}
      }
    }
  ]
}
lambda_handler(event, 1)