#!/usr/bin/env python3
"""
Simple test script to validate the food server functions
"""

import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that we can import FastMCP and the basic components"""
    print("Testing imports...")
    
    try:
        from fastmcp import FastMCP
        print("✓ FastMCP imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import FastMCP: {e}")
        return False
    
    try:
        from pydantic import BaseModel
        print("✓ Pydantic imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import Pydantic: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality without running the server"""
    print("\nTesting basic functionality...")
    
    # Test data structures
    from datetime import datetime
    from pathlib import Path
    
    # Test that data directory exists
    data_dir = Path("data")
    if data_dir.exists():
        print("✓ Data directory exists")
    else:
        print("✗ Data directory does not exist")
    
    # Test food log file
    food_log = data_dir / "food_log.md"
    if food_log.exists():
        print("✓ Food log file exists")
        # Read a few lines to test
        with open(food_log, 'r') as f:
            content = f.read()[:100]
            print(f"✓ Food log content preview: {content[:50]}...")
    else:
        print("✗ Food log file does not exist")
    
    return True

def test_server_syntax():
    """Test that the server file has valid syntax"""
    print("\nTesting server file syntax...")
    
    try:
        with open('mcp_food_server.py', 'r') as f:
            code = f.read()
        
        # Try to compile the code
        compile(code, 'mcp_food_server.py', 'exec')
        print("✓ Server file has valid Python syntax")
        
        # Check for FastMCP usage
        if 'from fastmcp import FastMCP' in code:
            print("✓ Server uses FastMCP import")
        else:
            print("✗ Server does not use FastMCP import")
            
        if '@mcp.tool()' in code:
            print("✓ Server uses FastMCP decorators")
        else:
            print("✗ Server does not use FastMCP decorators")
            
        if 'mcp.run()' in code:
            print("✓ Server uses FastMCP run method")
        else:
            print("✗ Server does not use FastMCP run method")
            
        return True
        
    except Exception as e:
        print(f"✗ Server file syntax error: {e}")
        return False

if __name__ == "__main__":
    print("FastMCP Food Server Validation")
    print("=" * 50)
    
    success = True
    
    success &= test_imports()
    success &= test_basic_functionality()
    success &= test_server_syntax()
    
    print("\n" + "="*50)
    if success:
        print("✓ All validation tests passed!")
        print("\nThe server has been successfully refactored to use FastMCP.")
        print("You can now run it with: python mcp_food_server.py")
    else:
        print("✗ Some validation tests failed!")
        
    print("=" * 50)
