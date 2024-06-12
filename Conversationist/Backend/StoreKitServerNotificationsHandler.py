import json
import boto3
import logging

# Initialize logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Log the received event
    logger.info("Received event: " + json.dumps(event, indent=2))
    
    # Parse the event data
    try:
        notification_type = event['notificationType']
        data = event['data']
    except KeyError as e:
        logger.error(f"Key error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f'Missing key in event data: {e}')
        }
    
    # Process the notification based on its type
    if notification_type == 'INITIAL_BUY':
        handle_initial_buy(data)
    elif notification_type == 'CANCEL':
        handle_cancel(data)
    # Add other notification types as needed
    else:
        logger.warning(f"Unhandled notification type: {notification_type}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processed notification successfully')
    }

def handle_initial_buy(data):
    # Implement logic to handle initial buy
    logger.info("Handling initial buy: ", data)
    # Example: Save to DynamoDB, trigger another Lambda, etc.

def handle_cancel(data):
    # Implement logic to handle cancel
    logger.info("Handling cancel: ", data)
    # Example: Update user subscription status in DynamoDB