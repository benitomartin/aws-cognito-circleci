import os

import boto3
import dotenv
from botocore.exceptions import ClientError
from loguru import logger

# Load environment variables
dotenv.load_dotenv()

AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")
USER_POOL_ID = os.getenv("USER_POOL_ID")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

# Create Cognito client
client = boto3.client(service_name="cognito-idp", region_name=AWS_REGION)

# Ensure required parameters are provided
if not USER_POOL_ID or not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
    raise ValueError("Missing one or more required environment variables: USER_POOL_ID, CLIENT_ID, CLIENT_SECRET")

# Check if Google Identity Provider exists
try:
    response = client.describe_identity_provider(UserPoolId=USER_POOL_ID, ProviderName="Google")
    logger.info("Google Identity Provider already exists")

    # Verify if the configuration matches
    provider_details = response["IdentityProvider"]["ProviderDetails"]
    if provider_details["client_id"] != GOOGLE_CLIENT_ID or provider_details["client_secret"] != GOOGLE_CLIENT_SECRET:
        logger.warning("Existing Google IdP has different client credentials. Updating...")
        client.update_identity_provider(
            UserPoolId=USER_POOL_ID,
            ProviderName="Google",
            ProviderDetails={
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "authorize_scopes": "openid email profile",
            },
            AttributeMapping={
                "email": "email",
                "username": "sub",
                "given_name": "given_name",
                "family_name": "family_name",
            },
        )
        logger.success("Google Identity Provider updated successfully")
    else:
        logger.info("Existing Google IdP configuration is up to date")

except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceNotFoundException":
        # Create Google identity provider if it doesn't exist
        try:
            logger.info("Creating new Google Identity Provider...")
            response = client.create_identity_provider(
                UserPoolId=USER_POOL_ID,
                ProviderName="Google",
                ProviderType="Google",
                ProviderDetails={
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "authorize_scopes": "openid email profile",
                },
                AttributeMapping={
                    "email": "email",
                    "username": "sub",
                    "given_name": "given_name",
                    "family_name": "family_name",
                },
            )
            logger.success("Successfully created Google Identity Provider")
        except ClientError as create_error:
            logger.error(f"Failed to create Google Identity Provider: {str(create_error)}")
            raise
    else:
        logger.error(f"Error checking Google Identity Provider: {str(e)}")
        raise
