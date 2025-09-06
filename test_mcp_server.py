import pytest
from fastapi.testclient import TestClient
from mcp_server import app, Meal, Ingredient
import os
from unittest.mock import patch, mock_open

client = TestClient(app)

@pytest.fixture(scope="module")
def test_data():
    return {
        "query": "I had a test meal",
        "meal_type": "Test",
        "date": "2025-01-01",
        "time": "12:00",
        "total_calories": 100.0,
        "total_protein_g": 10.0,
        "ingredients": [
            {
                "name": "Test Ingredient",
                "category": "Test Category",
                "calories": 100.0,
                "protein_g": 10.0,
            }
        ],
    }

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "MCP Food Log Server is running."}

def test_get_log():
    response = client.get("/get_log")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@patch("mcp_server.open", new_callable=mock_open)
def test_log_meal(mock_file, test_data):
    response = client.post("/log_meal", json=test_data)
    assert response.status_code == 200
    assert response.json() == {"status": "success"}

    mock_file.assert_called_with("data/food_log.md", "a")
    
    handle = mock_file()
    
    # Check that all the expected strings were written to the file
    handle.write.assert_any_call("### MEAL START\n")
    handle.write.assert_any_call("**Query:** I had a test meal\n")
    handle.write.assert_any_call("**Meal:** Test\n")
    handle.write.assert_any_call("**Date:** 2025-01-01\n")
    handle.write.assert_any_call("**Time:** 12:00\n")
    handle.write.assert_any_call("**Total Calories:** 100.0\n")
    handle.write.assert_any_call("**Total Protein (g):** 10.0\n")
    handle.write.assert_any_call("\n")
    handle.write.assert_any_call("| Ingredient | Category | Calories | Protein (g) |\n")
    handle.write.assert_any_call("|------------|----------|----------|-------------|\n")
    handle.write.assert_any_call("| Test Ingredient | Test Category | 100.0 | 10.0 |\n")
    handle.write.assert_any_call("### MEAL END\n\n")