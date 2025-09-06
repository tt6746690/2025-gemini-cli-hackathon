#!/usr/bin/env python3
"""
Simple test script to validate the FastMCP food server
"""

import tempfile
import shutil
from pathlib import Path
import sys
import importlib.util

# Import only the functions we need, not the server instance
spec = importlib.util.spec_from_file_location("mcp_food_server", "mcp_food_server.py")
mcp_module = importlib.util.module_from_spec(spec)

# Import without executing the main block
sys.modules["mcp_food_server"] = mcp_module
spec.loader.exec_module(mcp_module)

add_meal_to_log = mcp_module.add_meal_to_log
parse_food_log = mcp_module.parse_food_log

def test_add_meal():
    """Test adding a meal to the log"""
    print("Testing add_meal_to_log function...")
    
    meal_data = {
        "query": "I had a banana and yogurt for breakfast",
        "meal_type": "breakfast",
        "date": "2025-01-15",
        "time": "08:30",
        "ingredients": [
            {
                "name": "banana",
                "category": "fruit",
                "calories": 105,
                "protein_g": 1.3
            },
            {
                "name": "greek yogurt",
                "category": "dairy",
                "calories": 150,
                "protein_g": 15.0
            }
        ]
    }
    
    result = add_meal_to_log(meal_data)
    print(f"Add meal result: {result}")
    
    # Test parsing the log
    print("\nTesting parse_food_log function...")
    meals = parse_food_log()
    print(f"Found {len(meals)} meals in the log")
    
    if meals:
        latest_meal = meals[-1]
        print(f"Latest meal: {latest_meal.meal_type} on {latest_meal.date}")
        print(f"Ingredients: {[ing.name for ing in latest_meal.ingredients]}")

def test_basic_functions():
    """Test the basic functions work independently"""
    print("\n" + "="*50)
    print("Testing basic server functions...")
    
    # Test creating and accessing the tool functions directly
    from fastmcp import FastMCP
    
    # Create a test instance
    test_mcp = FastMCP("test-food-tracker")
    
    # Import the tool functions manually
    from mcp_food_server import (
        add_food_entry, get_food_log, 
        analyze_nutrition, search_food_entries
    )
    
    print("\n1. Testing add_food_entry function:")
    result1 = add_food_entry(
        query="Test meal with chicken and rice",
        ingredients=[
            {"name": "chicken breast", "calories": 165, "protein_g": 31},
            {"name": "brown rice", "calories": 216, "protein_g": 5}
        ],
        meal_type="lunch",
        date="2025-01-15",
        time="12:30"
    )
    print(f"Result: {result1}")
    
    print("\n2. Testing get_food_log function:")
    result2 = get_food_log(limit=2)
    print(f"Result: {result2}")
    
    print("\n3. Testing analyze_nutrition function:")
    result3 = analyze_nutrition(analysis_type="daily_summary")
    print(f"Result: {result3}")
    
    print("\n4. Testing search_food_entries function:")
    result4 = search_food_entries(search_term="chicken", search_type="ingredient")
    print(f"Result: {result4}")

if __name__ == "__main__":
    print("FastMCP Food Server Test")
    print("=" * 50)
    
    test_add_meal()
    test_basic_functions()
    
    print("\n" + "="*50)
    print("All tests completed!")
