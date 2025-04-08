# AWS Cognito CircleCI Integration

A Python-based tool for automating AWS Cognito User Pool setup and management through CircleCI pipelines.

## Features

- Automated creation and management of AWS Cognito User Pools
- User Pool Client configuration with OAuth 2.0 support
- Hosted UI domain setup
- Comprehensive logging with Loguru
- CircleCI integration ready

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
BOTO_SERVICE_NAME=cognito-idp
POOL_NAME=StreamlitAppUserPool
CLIENT_NAME=StreamlitAppClient
DOMAIN_PREFIX=streamlit-app
```

## Usage

Run the Cognito setup script:

```bash
uv run src/cognito.py
```

The script will:

1. Create or use existing Cognito User Pool
2. Set up App Client with OAuth configuration
3. Output the configuration details

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

XXX

## CircleCI Integration

The project includes CircleCI configuration for automated deployment. Configure the following environment variables in CircleCI:

- XXX

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.