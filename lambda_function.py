import json
import os
from package import requests



def lambda_handler(event, context):
    # Slack API endpoint
    url = "https://slack.com/api/chat.postMessage"

    # Slack API token (needs "chat:write" scope)
    token = os.environ['SLACK_TOKEN']

    # Slack channel to send message to
    channel = "#general"
    message = "Hello from Lambda!"

    # Construct payload
    payload = {
        "channel": channel,
        "text": message
    }

    # Set headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    # Make request to Slack API
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Print response
    #print(response.json())


lambda_handler(1,2)