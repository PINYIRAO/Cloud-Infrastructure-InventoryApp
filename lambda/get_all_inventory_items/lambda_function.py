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

        return {
            "statusCode": 200,
            "body": json.dumps(items, default=str),  # Handle Decimal etc.
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(str(e)),
        }
