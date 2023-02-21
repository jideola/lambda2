import json
from package import requests
from package import boto3
from package.exceptions import ClientError


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

