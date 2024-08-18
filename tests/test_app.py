import pytest
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    """
    Fixture to create a Flask test client that can be used to send requests to the application.
    """
    with app.test_client() as client:
        yield client


@patch("app.asset_service.get_paginated_assets")
def test_get_assets_success(mock_get_paginated_assets, client):
    """
    Test the /assets endpoint for a successful response with valid pagination parameters.
    """
    mock_get_paginated_assets.return_value = {
        "assets": [
            {"Name": "Test Asset", "Model": "Model X", "IP Address": "192.168.1.1"}
        ],
        "total": 1,
        "page": 1,
        "per_page": 5,
    }

    response = client.get("/assets?page=1&per_page=5")
    assert response.status_code == 200
    assert "assets" in response.json
    assert response.json["total"] == 1
    assert len(response.json["assets"]) == 1
    assert response.json["assets"][0]["Name"] == "Test Asset"


@patch("app.asset_service.get_paginated_assets")
def test_get_assets_no_pagination(mock_get_paginated_assets, client):
    """
    Test the /assets endpoint without pagination parameters to ensure defaults are used.
    """
    mock_get_paginated_assets.return_value = {
        "assets": [
            {"Name": "Test Asset", "Model": "Model X", "IP Address": "192.168.1.1"}
        ],
        "total": 1,
        "page": 1,
        "per_page": 5,
    }

    response = client.get("/assets")
    assert response.status_code == 200
    assert "assets" in response.json
    assert response.json["total"] == 1
    assert response.json["page"] == 1
    assert response.json["per_page"] == 5


@patch("app.asset_service.get_paginated_assets")
def test_get_assets_invalid_pagination(mock_get_paginated_assets, client):
    """
    Test the /assets endpoint with invalid pagination parameters to see if it handles errors.
    """
    response = client.get("/assets?page=invalid&per_page=5")
    assert response.status_code == 500
    assert "message" in response.json
    assert response.json["message"] == "Error fetching assets"


@patch("app.asset_service.find_asset_by_query")
def test_match_asset_success(mock_find_asset_by_query, client):
    """
    Test the /match endpoint for a successful asset search with a valid query.
    """
    mock_find_asset_by_query.return_value = {
        "Name": "Test Asset",
        "Model": "Model X",
        "IP Address": "192.168.1.1",
    }

    response = client.post("/match", json={"search": "Test"})
    assert response.status_code == 200
    assert "Name" in response.json
    assert response.json["Name"] == "Test Asset"
    assert response.json["IP Address"] == "192.168.1.1"


@patch("app.asset_service.find_asset_by_query")
def test_match_asset_no_match(mock_find_asset_by_query, client):
    """
    Test the /match endpoint when no asset matches the search query.
    """
    mock_find_asset_by_query.return_value = {"message": "No Asset Found"}

    response = client.post("/match", json={"search": "NonExistent"})
    assert response.status_code == 200
    assert "message" in response.json
    assert response.json["message"] == "No Asset Found"


@patch("app.asset_service.find_asset_by_query")
def test_match_asset_empty_query(mock_find_asset_by_query, client):
    """
    Test the /match endpoint with an empty search query.
    """
    mock_find_asset_by_query.return_value = {"message": "No Asset Found"}

    response = client.post("/match", json={"search": ""})
    assert response.status_code == 200
    assert "message" in response.json
    assert response.json["message"] == "No Asset Found"


@patch("app.asset_service.get_paginated_assets")
def test_get_assets_internal_error(mock_get_paginated_assets, client):
    """
    Test the /assets endpoint for handling an internal server error.
    """
    mock_get_paginated_assets.side_effect = Exception("Test Exception")

    response = client.get("/assets?page=1&per_page=5")
    assert response.status_code == 500
    assert "message" in response.json
    assert response.json["message"] == "Error fetching assets"


@patch("app.asset_service.find_asset_by_query")
def test_match_asset_internal_error(mock_find_asset_by_query, client):
    """
    Test the /match endpoint for handling an internal server error.
    """
    mock_find_asset_by_query.side_effect = Exception("Test Exception")

    response = client.post("/match", json={"search": "Test"})
    assert response.status_code == 500
    assert "message" in response.json
    assert response.json["message"] == "Error during search"
