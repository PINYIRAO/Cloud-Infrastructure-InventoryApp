import boto3
import json
import os
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):

    # Get the table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Get the key from the path parameters
    if 'pathParameters' not in event or 'location_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'location_id' path parameter")
        }

    key_value = int(event['pathParameters']['location_id'])

    # Get the item from the table
    try:

        response = table.query(IndexName = "GSI_location_id",KeyConditionExpression=Key("GSI_location_id").eq(key_value))

        item = response.get('Items', {})

        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }

        return {
            'statusCode': 200,
            'body': json.dumps(item, default=str)  # Use str to handle any special types like Decimal
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }