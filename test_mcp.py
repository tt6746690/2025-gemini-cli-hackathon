#!/usr/bin/env python3
"""
Test script to verify the MCP food server is working correctly.
"""

import asyncio
import json
from mcp.types import CallToolRequest, ListToolsRequest

# Import our server
from mcp_food_server import app


async def test_mcp_server():
    """Test the MCP server functionality."""
    print("🧪 Testing MCP Food Server...")
    
    # Test 1: List tools
    print("\n1️⃣ Testing list_tools...")
    tools_request = ListToolsRequest(method="tools/list")
    tools_result = await app.list_tools(tools_request)
    
    print(f"Available tools: {len(tools_result.tools)}")
    for tool in tools_result.tools:
        print(f"  - {tool.name}: {tool.description}")
    
    # Test 2: Add a food entry
    print("\n2️⃣ Testing add_food_entry...")
    add_request = CallToolRequest(
        method="tools/call",
        name="add_food_entry",
        arguments={
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
    )
    
    add_result = await app.call_tool(add_request)
    print(f"Add result: {add_result.content[0].text}")
    
    # Test 3: Get food log
    print("\n3️⃣ Testing get_food_log...")
    get_request = CallToolRequest(
        method="tools/call",
        name="get_food_log",
        arguments={"limit": 5}
    )
    
    get_result = await app.call_tool(get_request)
    print(f"Food log result:\n{get_result.content[0].text}")
    
    # Test 4: Analyze nutrition
    print("\n4️⃣ Testing analyze_nutrition...")
    analyze_request = CallToolRequest(
        method="tools/call",
        name="analyze_nutrition",
        arguments={"analysis_type": "daily_summary"}
    )
    
    analyze_result = await app.call_tool(analyze_request)
    print(f"Analysis result:\n{analyze_result.content[0].text}")
    
    print("\n✅ MCP Server test completed!")


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
