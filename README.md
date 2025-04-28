# AWS Cognito CircleCI Integration

A Python-based tool for automating AWS Cognito User Pool setup and management through CircleCI pipelines.

The project has been developed as part of the following [blog](XXXX)

## Features

- Automated creation and management of AWS Cognito User Pools
- User Pool Client configuration with OAuth 2.0 support
- Hosted UI domain setup
- Comprehensive logging with Loguru
- CircleCI integration ready

## Project Structure

```text
aws-cognito-circleci/
├── .circleci/
│   └── config.yml
├── app/
│   ├── __init__.py
│   ├── main.py
├── src/
│   ├── __init__.py
│   ├── cognito_app.py
│   ├── hosted_domain.py
│   ├── google_idp.py
│   └── client_login_pages.py
├── tests/
│   ├── test_cognito_app.py
│   └── test_streamlit_app.py
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── Makefile
├── README.md
├── pyproject.toml
└── uv.lock
```

## Prerequisites

- Python 3.12 or higher
- AWS account with appropriate permissions
- CircleCI account (for CI/CD integration)
- [UV package manager](https://docs.astral.sh/uv/)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/aws-cognito-circleci.git
cd aws-cognito-circleci
```

1. Create and activate a virtual environment:

```bash
uv sync --all-groups
source .venv/bin/activate
```

## Configuration

1. Create a `.env` file in the project root with the following variables:

```env
AWS_REGION=your-aws-region
POOL_NAME=StreamlitAppUserPool
CLIENT_NAME=StreamlitAppClient
CLIENT_ID=your-client-id
USER_POOL_ID=your-user-pool-id
DOMAIN_PREFIX=cog-app
REDIRECT_URI=http://localhost:8501
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## Usage

Run the Cognito setup script:

```bash
uv run src/cognito_app.py
```

The script will:

1. Create or use existing Cognito User Pool
1. Set up App Client with OAuth configuration
1. Output the configuration details, that shall be added to the `.env` file under `USER_POOL_ID` and `CLIENT_ID`

Run the Hosted UI domain setup script:

```bash
uv run src/hosted_domain.py
```

The script will:

1. Create or use existing Hosted UI domain
1. Output the domain URL

## Create a Google IDP

In the Google Cloud Console, create a new project and then navigate to `APIs & Services` -> `Credentials` -> `Create Credentials` -> `OAuth client ID`. Choose Web Application as the application type. Under Authorized redirect URIs, add the redirect URI for your Cognito Hosted UI, which is the domain of your Cognito Hosted UI + `/oauth2/idpresponse`: `https://<DOMAIN_PREFIX>.auth.<AWS_REGION>.amazoncognito.com/oauth2/idpresponse`.

Once created, copy the Client ID and Client Secret into your `.env` file as:

```.env
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

Then run the following command:

```bash
uv run src/google_idp.py
```

The script will:

1. Create a Google Identity Provider in your Cognito User Pool

## Activate Login with Google and Cognito User Pool

Once the Google Identity Provider is created, you need to update the User Pool Client to support Google as an identity provider. Run the following command:

```bash
uv run src/client_login_pages.py
```

The script will:

1. Update the User Pool Client to support Google as an identity provider
1. Update the User Pool Client to support Cognito User Pool as an identity provider

## Run the Streamlit App

Run the Streamlit app:

```bash
uv run streamlit run app/main.py
```

The app will:

1. Display a login button that redirects to the Cognito Hosted UI
1. After successful authentication, display the access and ID tokens

## Development

### Code Quality Tools

The project uses several tools to maintain code quality:

1. Run Ruff for linting:

```bash
make ruff
```

1. Run MyPy for type checking:

```bash
make mypy
```

1. Run all checks:

```bash
make all
```

### Testing

Run tests using pytest:

```bash
make test
```

## CircleCI Integration

The project includes CircleCI configuration for automated deployment. Configure the following environment variables in CircleCI:

```.env
AWS_REGION=your-aws-region
AWS_ACCESS_KEY_ID=your-aws-access-key-id
AWS_SECRET_ACCESS_KEY=your-aws-secret-access-key
POOL_NAME=StreamlitAppUserPool
CLIENT_NAME=StreamlitAppClient
CLIENT_ID=your-client-id
USER_POOL_ID=your-user-pool-id
DOMAIN_PREFIX=cog-app
REDIRECT_URI=http://localhost:8501
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
