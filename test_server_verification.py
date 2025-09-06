#!/usr/bin/env python3
"""
Simple test to verify the FastMCP server is working
"""

import sys
import os

def test_server_import():
    """Test that the server can be imported without hanging"""
    print("Testing server import...")
    
    try:
        # Import the server module without running it
        sys.path.insert(0, os.getcwd())
        
        # We'll test by checking if we can access the server's tools
        import importlib.util
        spec = importlib.util.spec_from_file_location("mcp_food_server", "mcp_food_server.py")
        server_module = importlib.util.module_from_spec(spec)
        
        # Prevent the server from running
        original_run = None
        
        # Execute the module
        spec.loader.exec_module(server_module)
        
        # Check if mcp instance exists and has tools
        if hasattr(server_module, 'mcp'):
            mcp = server_module.mcp
            print(f"✓ FastMCP server instance found: {mcp.name}")
            
            # Check if tools are registered
            if hasattr(mcp, '_tools') and mcp._tools:
                print(f"✓ Found {len(mcp._tools)} tools:")
                for tool_name in mcp._tools.keys():
                    print(f"  - {tool_name}")
                return True
            else:
                print("✗ No tools found in FastMCP server")
                return False
        else:
            print("✗ No FastMCP server instance found")
            return False
            
    except Exception as e:
        print(f"✗ Error importing server: {e}")
        return False

def test_tool_functions():
    """Test that the tool functions work independently"""
    print("\nTesting tool functions...")
    
    try:
        # Import the functions directly
        from mcp_food_server import add_food_entry, get_food_log, analyze_nutrition, search_food_entries
        
        print("✓ All tool functions imported successfully")
        
        # Test get_food_log (should work even with empty/existing data)
        result = get_food_log(limit=1)
        print(f"✓ get_food_log works: {result[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing tool functions: {e}")
        return False

if __name__ == "__main__":
    print("FastMCP Food Server Verification")
    print("=" * 50)
    
    success1 = test_server_import()
    success2 = test_tool_functions()
    
    print("\n" + "="*50)
    if success1 and success2:
        print("✅ FastMCP server is working correctly!")
        print("\nThe server should now work with Gemini CLI.")
        print("Try restarting Gemini CLI and the food-tracker should connect properly.")
    else:
        print("❌ FastMCP server has issues.")
        sys.exit(1)
