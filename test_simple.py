#!/usr/bin/env python3
"""
Simple test script to verify the food logging functions work correctly.
"""

import asyncio
from mcp_food_server import add_meal_to_log, parse_food_log


def test_food_functions():
    """Test the core food logging functionality."""
    print("🧪 Testing Food Logging Functions...")
    
    # Test 1: Add a food entry
    print("\n1️⃣ Testing add_meal_to_log...")
    meal_data = {
        "query": "I had a grilled chicken salad with avocado for lunch",
        "meal_type": "lunch",
        "date": "2025-09-06",
        "time": "12:30",
        "ingredients": [
            {
                "name": "Grilled Chicken Breast (6oz)",
                "category": "Protein",
                "calories": 280,
                "protein_g": 53,
                "carbs_g": 0,
                "fat_g": 6
            },
            {
                "name": "Mixed Greens (2 cups)",
                "category": "Vegetable",
                "calories": 20,
                "protein_g": 2,
                "carbs_g": 4,
                "fat_g": 0
            },
            {
                "name": "Avocado (1/2 medium)",
                "category": "Fat",
                "calories": 160,
                "protein_g": 2,
                "carbs_g": 9,
                "fat_g": 15
            }
        ]
    }
    
    result = add_meal_to_log(meal_data)
    print(f"Add result: {result}")
    
    # Test 2: Parse the food log
    print("\n2️⃣ Testing parse_food_log...")
    meals = parse_food_log()
    print(f"Found {len(meals)} meals in the log:")
    
    for i, meal in enumerate(meals[-3:], 1):  # Show last 3 meals
        print(f"  {i}. {meal.meal_type} on {meal.date} at {meal.time}")
        print(f"     Query: {meal.query}")
        print(f"     Calories: {meal.total_calories}, Protein: {meal.total_protein_g}g")
        print(f"     Ingredients: {len(meal.ingredients)} items")
    
    print("\n✅ Food logging test completed!")


if __name__ == "__main__":
    test_food_functions()
