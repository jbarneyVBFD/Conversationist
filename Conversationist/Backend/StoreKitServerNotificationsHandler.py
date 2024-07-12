import json
import logging
import base64
import boto3
from appstoreserverlibrary.api_client import AppStoreServerAPIClient, APIException
from appstoreserverlibrary.models.Environment import Environment
from appstoreserverlibrary.signed_data_verifier import VerificationException, SignedDataVerifier

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('YourDynamoDBTableName')

# Initialize App Store Server API
private_key = read_private_key("/path/to/key/SubscriptionKey_ABCDEFGHIJ.p8")
key_id = "ABCDEFGHIJ"
issuer_id = "99b16628-15e4-4668-972b-eeff55eeff55"
bundle_id = "com.example"
environment = Environment.SANDBOX

client = AppStoreServerAPIClient(private_key, key_id, issuer_id, bundle_id, environment)
root_certificates = load_root_certificates()
signed_data_verifier = SignedDataVerifier(root_certificates, enable_online_checks=True, environment=environment, bundle_id=bundle_id)

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event, indent=2))
    
    try:
        # Parse the body field to extract the JSON content
        body = json.loads(event['body'])
        signed_payload = body['signedPayload']
        
        # Verify and decode the signed payload
        payload = signed_data_verifier.verify_and_decode_notification(signed_payload)
        
        # Process the decoded payload
        notification_data = json.loads(payload)
        
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
    except VerificationException as e:
        logger.error(f"Verification error: {e}")
        return {
            'statusCode': 400,
            'body': json.dumps(f'Invalid notification signature: {e}')
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
    logger.info(f"Handling initial buy: {data}")
    # Extract relevant information from data
    email = data['email']
    password = data['password']
    subscription_status = data['subscriptionStatus']
    renewal_date = data['renewalDate']
    
    # Update DynamoDB
    table.update_item(
        Key={'email': email},
        UpdateExpression="SET password=:p, subscription_status=:s, renewal_date=:r",
        ExpressionAttributeValues={
            ':p': password,
            ':s': subscription_status,
            ':r': renewal_date
        }
    )

def handle_cancel(data):
    logger.info(f"Handling cancel: {data}")
    # Extract relevant information from data
    email = data['email']
    
    # Update DynamoDB
    table.update_item(
        Key={'email': email},
        UpdateExpression="SET subscription_status=:s",
        ExpressionAttributeValues={
            ':s': 'canceled'
        }
    )

def read_private_key(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def load_root_certificates():
    # Load the root certificates required for verification
    # Implementation to load certificates from the Apple PKI site
    pass

# Example structure for event
event = {
    "receipt_data": "MI..",  # Receipt data string
    "email": "user@example.com",
    "password": "securepassword"
}
