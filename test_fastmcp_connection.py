#!/usr/bin/env python3
"""
Test script to verify FastMCP server can start and list tools
"""

import asyncio
import sys
from fastmcp import Client

async def test_server():
    """Test that the server can start and respond to requests"""
    try:
        # Test by connecting to the server file directly
        async with Client("mcp_food_server.py") as client:
            print("✓ Successfully connected to FastMCP server")
            
            # List available tools
            tools = await client.list_tools()
            print(f"✓ Found {len(tools.tools)} tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Test a simple tool call
            result = await client.call_tool("get_food_log", {"limit": 1})
            print(f"✓ Tool call successful: {result.content[0].text[:100]}...")
            
            return True
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing FastMCP Food Server Connection")
    print("=" * 50)
    
    success = asyncio.run(test_server())
    
    if success:
        print("\n✓ FastMCP server is working correctly!")
        print("Your Gemini CLI should now be able to connect to the food-tracker server.")
    else:
        print("\n✗ FastMCP server test failed.")
        sys.exit(1)
