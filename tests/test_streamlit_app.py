import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from typing import Any
from unittest.mock import Mock, patch

import pytest

from app.main import exchange_code_for_tokens, get_auth_code


@pytest.fixture(autouse=True)
def mock_streamlit(mocker: Any) -> None:
    mocker.patch("app.main.st")


@patch("app.main.requests.post")
def test_exchange_code_for_tokens_success(mock_post: Mock) -> None:
    """Test successful token exchange with valid authorization code."""
    mock_response = mock_post.return_value
    mock_response.status_code = 200
    mock_response.json.return_value = {"access_token": "fake_access_token", "id_token": "fake_id_token"}

    result_tokens: dict[str, str] | None = exchange_code_for_tokens("test_code")
    assert result_tokens is not None
    assert result_tokens["access_token"] == "fake_access_token"
    assert result_tokens["id_token"] == "fake_id_token"
    print("✅ Token exchange successful.")


@patch("app.main.requests.post")
def test_exchange_code_for_tokens_failure(mock_post: Mock) -> None:
    """Test failed token exchange with invalid authorization code."""
    mock_response = mock_post.return_value
    mock_response.status_code = 400
    mock_response.text = "Bad request"

    result_tokens: dict[str, str] | None = exchange_code_for_tokens("bad_code")
    assert result_tokens is None
    print("✅ Token exchange failed as expected.")


def test_get_auth_code_success(mocker: Any) -> None:
    """Test successful retrieval of authorization code from query parameters."""
    mocker.patch("app.main.st.query_params", {"code": "test_auth_code"})
    auth_code: str | None = get_auth_code()
    assert auth_code == "test_auth_code"
    print("✅ Authorization code retrieved successfully.")


def test_get_auth_code_missing(mocker: Any) -> None:
    """Test handling of missing authorization code in query parameters."""
    mocker.patch("app.main.st.query_params", {})
    auth_code: str | None = get_auth_code()
    assert auth_code is None
    print("✅ Missing authorization code handled successfully.")
