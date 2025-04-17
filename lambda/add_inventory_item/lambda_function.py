import json
import logging
import os
from decimal import Decimal

import boto3
from ulid import ULID

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def lambda_handler(event, context):
    # Parse incoming JSON data, this is a test modification, change back
    try:
        # Ensure 'body' exists and parse it
        if "body" not in event:
            return {
                "statusCode": 400,
                "body": json.dumps("Bad request. No body provided."),
            }

        data = json.loads(event["body"], parse_float=Decimal)

        # Validate required fields in the data
        required_fields = ["name", "description", "qty", "price", "location_id"]
        for field in required_fields:
            if field not in data:
                return {
                    "statusCode": 400,
                    "body": json.dumps(f"Bad request. Missing '{field}' field."),
                }

    except KeyError as e:
        logger.error(f"Missing key: {e}")
        return {
            "statusCode": 400,
            "body": json.dumps("Bad request. Please provide the data."),
        }
    except json.JSONDecodeError:
        logger.error("Failed to parse JSON body")
        return {
            "statusCode": 400,
            "body": json.dumps("Bad request. Invalid JSON format."),
        }

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

    # Get the table name from environment variable, otherwise use the default table name
    table_name = os.getenv("TABLE_NAME", "Inventory")

    # DynamoDB setup
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    # Generate a unique ID using the ulid module
    unique_id = str(ULID())

    # Insert data into DynamoDB
    try:
        table.put_item(
            Item={
                "id": unique_id,
                "GSI_id": unique_id,
                "name": data["name"],
                "description": data["description"],
                "qty": data["qty"],
                "price": data["price"],
                "location_id": data["location_id"],
                "GSI_location_id": data["location_id"],
            }
        )
        logger.info(f"Item {data['name']} with ID {unique_id} added successfully.")
        return {
            "statusCode": 200,
            'headers': headers,
            "body": json.dumps(
                f"Item {data['name']} with ID {unique_id} added successfully."
            ),
        }
    except Exception as e:
        logger.error(f"Error adding item: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Error adding item: {str(e)}"),
        }
