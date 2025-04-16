import json
import os

import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    """
    AWS Lambda function to delete an item from DynamoDB using its ID.
    """
    table_name = os.getenv("TABLE_NAME", "Inventory")
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    # Validate path parameter
    path_params = event.get("pathParameters", {})
    key_value = path_params.get("id")

    if not key_value:
        return {
            "statusCode": 400,
            "body": json.dumps("Missing 'id' path parameter"),
        }

    try:
        response = table.query(KeyConditionExpression=Key("id").eq(key_value))

        for item in response.get("Items", []):
            table.delete_item(
                Key={
                    "id": item["id"],
                    "location_id": item["location_id"],
                }
            )

        return {
            "statusCode": 200,
            "body": json.dumps(f"Item with ID {key_value} deleted successfully."),
        }

    except Exception as e:
        print(e)
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error deleting item: {str(e)}"),
        }
