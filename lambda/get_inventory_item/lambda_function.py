import json
import os

import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    """
    Lambda function to retrieve an item from DynamoDB by ID.
    """
    table_name = os.getenv("TABLE_NAME", "Inventory")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    if "pathParameters" not in event or "id" not in event["pathParameters"]:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' path parameter"),
        }

    key_value = event["pathParameters"]["id"]

    try:
        response = table.query(KeyConditionExpression=Key("id").eq(key_value))
        items = response.get("Items", [])

        # Define allowed CORS headers
        headers = {
            "Access-Control-Allow-Origin": "*",  # Allow all origins
            "Access-Control-Allow-Methods": "GET, POST, DELETE, OPTIONS",  # Allowed HTTP methods
            "Access-Control-Allow-Headers": "Content-Type"  # Allowed request headers
        }

        # Check if the request method is OPTIONS (CORS pre-flight request)
        if event['httpMethod'] == 'OPTIONS':
            # Return 200 response for OPTIONS requests with CORS headers
            return {
                'statusCode': 200,
                'headers': headers,
                'body': 'CORS pre-flight response'  # Optional body for pre-flight request
            }

        if not items:
            return {
                "statusCode": 404,
                "body": json.dumps("Item not found"),
            }

        return {
            "statusCode": 200,
            'headers': headers,
            "body": json.dumps(items, default=str),
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(str(e)),
        }
