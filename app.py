import os

import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up constants from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
DOMAIN_PREFIX = os.getenv("DOMAIN_PREFIX")
AWS_REGION = os.getenv("AWS_REGION")
COGNITO_DOMAIN = f"https://{DOMAIN_PREFIX}.auth.{AWS_REGION}.amazoncognito.com"

# Cognito token endpoint
TOKEN_URL = f"{COGNITO_DOMAIN}/oauth2/token"

# Handle redirect URI (authorization code flow) 
def get_auth_code() -> str | None: 
    # Use st.query_params instead of the deprecated experimental function
    query_params = st.query_params
    # Debug: Print the query parameters to see what we're receiving
    # st.write("Debug - Query parameters:", query_params)
    code = query_params.get("code", None)
    # Debug: Print the code value
    # st.write("Debug - Auth code received:", code)
    return code 

# Exchange the authorization code for tokens
def exchange_code_for_tokens(auth_code: str) -> dict[str, str] | None:
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        # 'client_secret': os.getenv("CLIENT_SECRET", "")
    }

    response = requests.post(TOKEN_URL, data=data)
    if response.status_code == 200:
        tokens = response.json()
        return dict(tokens)
    else:
        st.error("Failed to get tokens")
        return None

# Main app
def main() -> None:
    # Check if user is already authenticated
    auth_code = get_auth_code()

    if auth_code:
        # Exchange auth code for tokens
        tokens = exchange_code_for_tokens(auth_code)

        if tokens:
            st.success("Successfully authenticated!")
            st.write("Access Token:", tokens['access_token'])
            st.write("ID Token:", tokens['id_token'])
        else:
            st.error("Failed to authenticate.")
    else:
        # Show the login button to redirect to Cognito Hosted UI
        st.title("Welcome to Streamlit App!")
        st.write("Please log in to continue.")
        cognito_url = f"{COGNITO_DOMAIN}/login?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=email+openid+profile"
        st.markdown(f"[Login with Cognito]({cognito_url})")

if __name__ == "__main__":
    main()
