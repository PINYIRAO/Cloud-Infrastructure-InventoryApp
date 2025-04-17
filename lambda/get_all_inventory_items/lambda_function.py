import json
import os

import boto3


def lambda_handler(event, context):
    """
    AWS Lambda function to scan all items from a DynamoDB table.
    """
    table_name = os.getenv("TABLE_NAME", "Inventory")
    dynamo_client = boto3.client("dynamodb")

    try:
        response = dynamo_client.scan(TableName=table_name)
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

        return {
            "statusCode": 200,
            'headers': headers,
            "body": json.dumps(items, default=str),  # Handle Decimal etc.
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(str(e)),
        }
