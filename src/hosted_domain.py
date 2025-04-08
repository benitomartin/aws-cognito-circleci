import os

import boto3
import dotenv
from botocore.exceptions import ClientError
from loguru import logger

dotenv.load_dotenv()

domain_name = "hellokitty"

AWS_REGION = os.getenv('AWS_REGION')
BOTO_SERVICE_NAME = os.getenv('BOTO_SERVICE_NAME', 'cognito-idp')
POOL_NAME = os.getenv('POOL_NAME')
DOMAIN_PREFIX = domain_name

if not AWS_REGION:
    raise ValueError("Missing AWS_REGION in .env file")

# Set up logging
logger.info("Starting Hosted UI Domain setup script...")

# Create Cognito client
client = boto3.client(service_name=BOTO_SERVICE_NAME, region_name=AWS_REGION)

# Step 1: Check if the user pool exists and get its ID
logger.info(f"Checking if user pool '{POOL_NAME}' exists...")

existing_pool_id = None
paginator = client.get_paginator('list_user_pools')
for page in paginator.paginate(MaxResults=60):
    for pool in page['UserPools']:
        if pool['Name'] == POOL_NAME:
            existing_pool_id = pool['Id']
            logger.info(f"User pool '{POOL_NAME}' exists with ID: {existing_pool_id}")
            break
    if existing_pool_id:
        break

if not existing_pool_id:
    logger.error(f"User pool '{POOL_NAME}' does not exist.")
    raise ValueError(f"User pool '{POOL_NAME}' not found. Please create it first.")
else:
    user_pool_id = existing_pool_id

# Step 3: Create the Hosted UI domain if it doesn't exist
try:
    logger.info(f"Creating new Hosted UI domain '{DOMAIN_PREFIX}'...")
    response_domain = client.create_user_pool_domain(
        Domain=DOMAIN_PREFIX,
        UserPoolId=user_pool_id
    )
    logger.success(f"Hosted UI domain created: https://{DOMAIN_PREFIX}.auth.{AWS_REGION}.amazoncognito.com")

except ClientError as exception:
    logger.error(f"Error creating Hosted UI domain: {exception}")
    raise

# Final output
logger.info("Hosted UI domain setup completed successfully.")
logger.info(f"Hosted UI domain URL: https://{DOMAIN_PREFIX}.auth.{AWS_REGION}.amazoncognito.com")
