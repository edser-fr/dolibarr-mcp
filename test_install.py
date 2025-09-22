#!/usr/bin/env python3
"""Quick test to verify Dolibarr MCP installation."""

def test_installation():
    """Test if the Dolibarr MCP installation is working."""
    print("\n" + "="*50)
    print("Testing Dolibarr MCP Installation")
    print("="*50 + "\n")
    
    # Test 1: Import main modules
    print("1. Testing module imports...")
    try:
        from dolibarr_mcp.config import Config
        print("   [OK] dolibarr_mcp.config")
    except ImportError as e:
        print(f"   [FAIL] dolibarr_mcp.config: {e}")
        return False
    
    try:
        from dolibarr_mcp.dolibarr_client import DolibarrClient
        print("   [OK] dolibarr_mcp.dolibarr_client")
    except ImportError as e:
        print(f"   [FAIL] dolibarr_mcp.dolibarr_client: {e}")
        return False
    
    try:
        from dolibarr_mcp.dolibarr_mcp_server import DolibarrMCPServer
        print("   [OK] dolibarr_mcp.dolibarr_mcp_server")
    except ImportError as e:
        print(f"   [FAIL] dolibarr_mcp.dolibarr_mcp_server: {e}")
        return False
    
    # Test 2: Check dependencies
    print("\n2. Testing dependencies...")
    try:
        import mcp
        print("   [OK] mcp")
    except ImportError:
        print("   [FAIL] mcp - Run: pip install mcp")
        return False
    
    try:
        import aiohttp
        print("   [OK] aiohttp")
    except ImportError:
        print("   [FAIL] aiohttp - Run: pip install aiohttp")
        return False
    
    try:
        import pydantic
        print("   [OK] pydantic")
    except ImportError:
        print("   [FAIL] pydantic - Run: pip install pydantic")
        return False
    
    try:
        import dotenv
        print("   [OK] python-dotenv")
    except ImportError:
        print("   [FAIL] python-dotenv - Run: pip install python-dotenv")
        return False
    
    # Test 3: Check configuration
    print("\n3. Testing configuration...")
    import os
    if os.path.exists(".env"):
        print("   [OK] .env file exists")
        try:
            config = Config()
            print("   [OK] Config loaded successfully")
            if config.dolibarr_url == "https://your-dolibarr-instance.com/api/index.php":
                print("   [!] WARNING: Using default URL - Please update .env file")
            if config.dolibarr_api_key == "your_api_key_here":
                print("   [!] WARNING: Using default API key - Please update .env file")
        except Exception as e:
            print(f"   [FAIL] Config loading error: {e}")
    else:
        print("   [!] .env file not found - Create one from .env.example")
    
    print("\n" + "="*50)
    print("[SUCCESS] Installation test passed!")
    print("="*50)
    print("\nNext steps:")
    print("1. Edit .env file with your Dolibarr credentials")
    print("2. Run: python -m dolibarr_mcp")
    print("3. Or test connection: python test_connection.py")
    
    return True

if __name__ == "__main__":
    import sys
    if not test_installation():
        sys.exit(1)
