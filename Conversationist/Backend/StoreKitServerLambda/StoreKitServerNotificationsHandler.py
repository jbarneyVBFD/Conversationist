import json
import logging
import base64
import jwt  # PyJWT library
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# You need to install the `PyJWT` library and include it in your Lambda package
# pip install pyjwt -t .

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))
    
    try:
        # Parse the body field to extract the JSON content
        body = json.loads(event['body'])
        signed_payload = body['signedPayload']
        
        # Decode the JWS (JSON Web Signature) payload
        header, payload, signature = decode_jws(signed_payload)
        
        # Process the decoded payload
        notification_data = json.loads(base64url_decode(payload))
        
        notification_type = notification_data['notificationType']
        data = notification_data['data']
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
    except Exception as e:
        logger.error(f"General error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error processing notification: {e}')
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
    logger.info("Handling initial buy: ", data)
    # Implement your logic here, e.g., updating a database

def handle_cancel(data):
    logger.info("Handling cancel: ", data)
    # Implement your logic here, e.g., updating a database

def decode_jws(jws):
    parts = jws.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid JWS format")
    return parts[0], parts[1], parts[2]

def base64url_decode(input):
    # Add padding if needed
    input += '=' * (4 - len(input) % 4)
    return base64.urlsafe_b64decode(input)
