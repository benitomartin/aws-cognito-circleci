import os

import boto3
import dotenv
from loguru import logger

# Load environment variables
dotenv.load_dotenv()

AWS_REGION = os.getenv('AWS_REGION', 'eu-central-1')
USER_POOL_ID = os.getenv('USER_POOL_ID')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')  

# Create Cognito client
client = boto3.client(service_name='cognito-idp', region_name=AWS_REGION)

# Ensure required parameters are provided
if not USER_POOL_ID or not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise ValueError("Missing one or more required environment variables: USER_POOL_ID, CLIENT_ID, CLIENT_SECRET")

# Create Google identity provider
try:
    response = client.create_identity_provider(
        UserPoolId=USER_POOL_ID,
        ProviderName='Google',
        ProviderType='Google',
        ProviderDetails={
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,  
            'authorize_scopes': 'openid email profile',  
        },
        AttributeMapping={
            'email': 'email',
            'username': 'sub',
            'given_name': 'given_name',
            'family_name': 'family_name',
        }
    )
    logger.success("Successfully created Google Identity Provider")
    logger.info(f"Response: {response}")
except Exception as e:
    logger.error(f"Failed to create Google Identity Provider: {str(e)}")
    raise
