# AWS Cognito CircleCI Integration

A Python-based tool for automating AWS Cognito User Pool setup and management through CircleCI pipelines.

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
│   ├── __init__.py
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

First you need to create a Google Client in the Google Cloud Console. First you need to create a project. The, under `APIs & Services` -> `Credentials` create a new OAuth client ID. You need to select Web Application as the application type and add the following redirect URI, which is the domain of your Cognito Hosted UI + `/oauth2/idpresponse`: `https://cog-app.auth.eu-central-1.amazoncognito.com/oauth2/idpresponse`.

Once you click on `Create`, you will get the client ID and client secret. Add them to the `.env` file under `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`.

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

- XXXX

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
