import os

import boto3
import dotenv

dotenv.load_dotenv()

USER_POOL_ID = os.getenv("USER_POOL_ID")
CLIENT_ID = os.getenv("CLIENT_ID")

client = boto3.client("cognito-idp")

client.update_user_pool_client(
    UserPoolId=USER_POOL_ID,
    ClientId=CLIENT_ID,
    SupportedIdentityProviders=["COGNITO", "Google"],
    CallbackURLs=["http://localhost:8501"],
    LogoutURLs=["http://localhost:8501/logout"],
    AllowedOAuthFlows=["code"],
    AllowedOAuthScopes=["email", "openid", "profile"],
    AllowedOAuthFlowsUserPoolClient=True,
)
