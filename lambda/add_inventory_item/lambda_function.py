import json
import boto3
import uuid
import os
from ulid import ULID

def lambda_handler(event, context):
    # Parse incoming JSON data
    try:
        data = json.loads(event['body'])
    except KeyError:
        return {
            'statusCode': 400,
            'body': json.dumps("Bad request. Please provide the data.")
        }

    # Get the table name from environment variable, otherwise use the default table name
    table_name = os.getenv('TABLE_NAME', 'Inventory')

    # DynamoDB setup
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)

    # Generate a unique ID using the ulid module
    unique_id = str(ULID())

    # Insert data into DynamoDB
    try:
        table.put_item(
            Item={
                'id': unique_id,
                'GSI_id': unique_id,
                'name': data['name'],
                'description': data['description'],
                'qty': data['qty'],
                'price': data['price'],
                'location_id': data['location_id'],
                'GSI_location_id': data['location_id']

            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps(f"Item {data['name']} with ID {unique_id} added successfully.")
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error adding item: {str(e)}")
        }