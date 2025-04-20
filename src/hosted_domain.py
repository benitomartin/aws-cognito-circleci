import os

import boto3
import dotenv
from botocore.exceptions import ClientError
from loguru import logger

dotenv.load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
POOL_NAME = os.getenv("POOL_NAME")
DOMAIN_PREFIX = os.getenv("DOMAIN_PREFIX")

if not AWS_REGION:
    raise ValueError("Missing AWS_REGION in .env file")
if not POOL_NAME:
    raise ValueError("Missing POOL_NAME in .env file")
if not DOMAIN_PREFIX:
    raise ValueError("Missing DOMAIN_PREFIX in .env file")

# Set up logging
logger.info("Starting Hosted UI Domain setup script...")

# Create Cognito client
client = boto3.client(service_name="cognito-idp", region_name=AWS_REGION)

# Step 1: Check if the user pool exists and get its ID
logger.info(f"Checking if user pool '{POOL_NAME}' exists...")

existing_pool_id = None
paginator = client.get_paginator("list_user_pools")
for page in paginator.paginate(MaxResults=60, PaginationConfig={"MaxItems": 10}):  # type: ignore
    for pool in page["UserPools"]:
        if pool["Name"] == POOL_NAME:
            existing_pool_id = pool["Id"]
            logger.info(f"User pool '{POOL_NAME}' exists with ID: {existing_pool_id}")
            break
    if existing_pool_id:
        break

if not existing_pool_id:
    logger.error(f"User pool '{POOL_NAME}' does not exist.")
    raise ValueError(f"User pool '{POOL_NAME}' not found. Please create it first.")

user_pool_id = existing_pool_id

# Step 2: Check if domain already exists
try:
    response = client.describe_user_pool_domain(Domain=DOMAIN_PREFIX)
    domain_description = response.get("DomainDescription", {})

    if domain_description.get("Domain") == DOMAIN_PREFIX and domain_description.get("Status") == "ACTIVE":
        logger.info(f"Hosted UI domain '{DOMAIN_PREFIX}' already exists and is active")
    else:
        # Create the domain since the description is empty
        try:
            logger.info(f"Creating new Hosted UI domain '{DOMAIN_PREFIX}'...")
            client.create_user_pool_domain(Domain=DOMAIN_PREFIX, UserPoolId=user_pool_id)
            logger.success(f"Hosted UI domain created: https://{DOMAIN_PREFIX}.auth.{AWS_REGION}.amazoncognito.com")
        except ClientError as create_error:
            logger.error(f"Error creating Hosted UI domain: {create_error}")
            raise
except ClientError as e:
    if e.response["Error"]["Code"] == "ResourceNotFoundException":
        # Step 3: Create the Hosted UI domain if it doesn't exist
        try:
            logger.info(f"Creating new Hosted UI domain '{DOMAIN_PREFIX}'...")
            client.create_user_pool_domain(Domain=DOMAIN_PREFIX, UserPoolId=user_pool_id)
            logger.success(f"Hosted UI domain created: https://{DOMAIN_PREFIX}.auth.{AWS_REGION}.amazoncognito.com")
        except ClientError as create_error:
            logger.error(f"Error creating Hosted UI domain: {create_error}")
            raise
    else:
        logger.error(f"Error checking domain existence: {e}")
        raise

# Final output
domain_url = f"https://{DOMAIN_PREFIX}.auth.{AWS_REGION}.amazoncognito.com"
logger.info("Hosted UI domain setup completed successfully.")
logger.info(f"Hosted UI domain URL: {domain_url}")
