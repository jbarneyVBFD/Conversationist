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
        body = json.loads(event['body'])
        notification_type = body['notificationType']
        data = body['data']
    except KeyError as e:
        logger.error(f"Key error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f'Missing key in event data: {e}')
        }
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f'Invalid JSON in event body: {e}')
        }
    
    try:
        if notification_type == 'INITIAL_BUY':
            handle_initial_buy(data)
        elif notification_type == 'CANCEL':
            handle_cancel(data)
        else:
            logger.warning(f"Unhandled notification type: {notification_type}")
            return {
                'statusCode': 400,
                'body': json.dumps(f'Unhandled notification type: {notification_type}')
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps('Processed notification successfully')
        }
    except Exception as e:
        logger.error(f"Processing error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing notification: {e}')
        }

def handle_initial_buy(data):
    # Implement logic to handle initial buy
    logger.info("Handling initial buy: ", data)
    # Example: Save to DynamoDB, trigger another Lambda, etc.

def handle_cancel(data):
    # Implement logic to handle cancel
    logger.info("Handling cancel: ", data)
    # Example: Update user subscription status in DynamoDB
