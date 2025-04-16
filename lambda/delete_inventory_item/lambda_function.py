import boto3
import json
import os
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamo_client = boto3.client('dynamodb')

    # Get the table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Extract the '_id' from the path parameters
    if 'pathParameters' not in event or 'id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    key_value = event['pathParameters']['id']


    # Attempt to delete the item from the table
    try:
        response = table.query(KeyConditionExpression=Key("id").eq(key_value))
        for item in response['Items']:
            table.delete_item(Key={
                "id":item["id"],
                "location_id":item["location_id"]
            })
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {key_value} deleted successfully.")
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }