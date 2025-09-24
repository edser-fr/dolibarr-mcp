"""Ultra-simple Dolibarr server - Zero compiled extensions, maximum Windows compatibility."""

import json
import sys
import os
import logging
from typing import Any, Dict, List, Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Import our ultra-simple components (no compiled extensions)
from src.dolibarr_mcp.simple_client import SimpleDolibarrClient, SimpleDolibarrAPIError, SimpleConfig

# Configure logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)

class UltraSimpleServer:
    """Ultra-simple server implementation - pure Python, zero compiled extensions."""
    
    def __init__(self, name: str = "dolibarr-mcp-ultra"):
        self.name = name
        self.logger = logging.getLogger(__name__)
        self.client = None
        
    def init_client(self):
        """Initialize the Dolibarr client."""
        if not self.client:
            config = SimpleConfig()
            self.client = SimpleDolibarrClient(config)
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names."""
        return [
            "test_connection",
            "get_status", 
            "get_users",
            "get_user_by_id",
            "create_user",
            "update_user", 
            "delete_user",
            "get_customers",
            "get_customer_by_id",
            "create_customer",
            "update_customer",
            "delete_customer",
            "get_products",
            "get_product_by_id", 
            "create_product",
            "update_product",
            "delete_product",
            "raw_api"
        ]
    
    def handle_tool_call(self, tool_name: str, arguments: dict) -> Dict[str, Any]:
        """Handle tool calls using the simple client."""
        
        try:
            self.init_client()
            
            # System tools
            if tool_name == "test_connection":
                result = self.client.get_status()
                if 'success' not in result:
                    result = {"status": "success", "message": "API connection working", "data": result}
                return {"success": True, "data": result}
            
            elif tool_name == "get_status":
                result = self.client.get_status()
                return {"success": True, "data": result}
            
            # User management
            elif tool_name == "get_users":
                result = self.client.get_users(
                    limit=arguments.get('limit', 100),
                    page=arguments.get('page', 1)
                )
                return {"success": True, "data": result}
            
            elif tool_name == "get_user_by_id":
                result = self.client.get_user_by_id(arguments['user_id'])
                return {"success": True, "data": result}
            
            elif tool_name == "create_user":
                result = self.client.create_user(**arguments)
                return {"success": True, "data": result}
            
            elif tool_name == "update_user":
                user_id = arguments.pop('user_id')
                result = self.client.update_user(user_id, **arguments)
                return {"success": True, "data": result}
            
            elif tool_name == "delete_user":
                result = self.client.delete_user(arguments['user_id'])
                return {"success": True, "data": result}
            
            # Customer management
            elif tool_name == "get_customers":
                result = self.client.get_customers(
                    limit=arguments.get('limit', 100),
                    page=arguments.get('page', 1)
                )
                return {"success": True, "data": result}
            
            elif tool_name == "get_customer_by_id":
                result = self.client.get_customer_by_id(arguments['customer_id'])
                return {"success": True, "data": result}
            
            elif tool_name == "create_customer":
                result = self.client.create_customer(**arguments)
                return {"success": True, "data": result}
            
            elif tool_name == "update_customer":
                customer_id = arguments.pop('customer_id')
                result = self.client.update_customer(customer_id, **arguments)
                return {"success": True, "data": result}
            
            elif tool_name == "delete_customer":
                result = self.client.delete_customer(arguments['customer_id'])
                return {"success": True, "data": result}
            
            # Product management
            elif tool_name == "get_products":
                result = self.client.get_products(limit=arguments.get('limit', 100))
                return {"success": True, "data": result}
            
            elif tool_name == "get_product_by_id":
                result = self.client.get_product_by_id(arguments['product_id'])
                return {"success": True, "data": result}
            
            elif tool_name == "create_product":
                result = self.client.create_product(**arguments)
                return {"success": True, "data": result}
            
            elif tool_name == "update_product":
                product_id = arguments.pop('product_id')
                result = self.client.update_product(product_id, **arguments)
                return {"success": True, "data": result}
            
            elif tool_name == "delete_product":
                result = self.client.delete_product(arguments['product_id'])
                return {"success": True, "data": result}
            
            # Raw API access
            elif tool_name == "raw_api":
                result = self.client.raw_api(**arguments)
                return {"success": True, "data": result}
            
            else:
                return {"error": f"Unknown tool: {tool_name}", "type": "unknown_tool"}
        
        except SimpleDolibarrAPIError as e:
            return {"error": f"Dolibarr API Error: {str(e)}", "type": "api_error"}
        
        except Exception as e:
            self.logger.error(f"Tool execution error: {e}")
            return {"error": f"Tool execution failed: {str(e)}", "type": "internal_error"}
    
    def format_response(self, content: Dict[str, Any]) -> str:
        """Format response as JSON string."""
        return json.dumps(content, indent=2, ensure_ascii=False)
    
    def run_interactive(self):
        """Run server in interactive mode for testing."""
        print("🚀 Ultra-Simple Dolibarr MCP Server (Maximum Windows Compatibility)", file=sys.stderr)
        print("✅ ZERO compiled extensions - NO .pyd files!", file=sys.stderr)
        print("✅ Only pure Python + requests library", file=sys.stderr)
        print("", file=sys.stderr)
        
        # Test configuration
        try:
            config = SimpleConfig()
            
            if "your-dolibarr-instance" in config.dolibarr_url:
                print("⚠️  DOLIBARR_URL not configured in .env file", file=sys.stderr)
                print("📝 Please edit .env with your Dolibarr credentials", file=sys.stderr)
            elif "placeholder_api_key" in config.api_key:
                print("⚠️  DOLIBARR_API_KEY not configured in .env file", file=sys.stderr)
                print("📝 Please edit .env with your Dolibarr API key", file=sys.stderr)
            else:
                print("🧪 Testing Dolibarr API connection...", file=sys.stderr)
                test_result = self.handle_tool_call("test_connection", {})
                if test_result.get("success"):
                    print("✅ Dolibarr API connection successful!", file=sys.stderr)
                else:
                    print(f"⚠️  API test result: {test_result}", file=sys.stderr)
                    
        except Exception as e:
            print(f"⚠️  Configuration error: {e}", file=sys.stderr)
        
        print("", file=sys.stderr)
        print("📋 Available Tools:", file=sys.stderr)
        tools = self.get_available_tools()
        for i, tool in enumerate(tools, 1):
            print(f"  {i:2}. {tool}", file=sys.stderr)
        
        print("", file=sys.stderr)
        print("💡 Interactive Testing Mode:", file=sys.stderr)
        print("   Type 'list' to see all tools", file=sys.stderr)
        print("   Type 'test <tool_name>' to test a tool", file=sys.stderr)
        print("   Type 'help' for more commands", file=sys.stderr)
        print("   Type 'exit' to quit", file=sys.stderr)
        print("", file=sys.stderr)
        
        while True:
            try:
                command = input("dolibarr-ultra> ").strip()
                
                if command == "exit":
                    break
                    
                elif command == "list":
                    print("Available tools:")
                    for i, tool in enumerate(tools, 1):
                        print(f"  {i:2}. {tool}")
                
                elif command == "help":
                    print("Commands:")
                    print("  list                    - Show all available tools")
                    print("  test <tool_name>        - Test a specific tool")
                    print("  config                  - Show current configuration")
                    print("  exit                    - Quit the server")
                    print("")
                    print("Quick tests available:")
                    print("  test test_connection    - Test API connection")
                    print("  test get_status         - Get Dolibarr status")
                    print("  test get_users          - Get first 5 users")
                    print("  test get_customers      - Get first 5 customers")
                    print("  test get_products       - Get first 5 products")
                
                elif command == "config":
                    config = SimpleConfig()
                    print(f"Configuration:")
                    print(f"  URL: {config.dolibarr_url}")
                    print(f"  API Key: {'*' * min(len(config.api_key), 10)}...")
                    print(f"  Log Level: {config.log_level}")
                    
                elif command.startswith("test "):
                    tool_name = command[5:].strip()
                    
                    # Quick test implementations
                    if tool_name == "test_connection":
                        result = self.handle_tool_call("test_connection", {})
                    elif tool_name == "get_status":
                        result = self.handle_tool_call("get_status", {})
                    elif tool_name == "get_users":
                        result = self.handle_tool_call("get_users", {"limit": 5})
                    elif tool_name == "get_customers":
                        result = self.handle_tool_call("get_customers", {"limit": 5})
                    elif tool_name == "get_products":
                        result = self.handle_tool_call("get_products", {"limit": 5})
                    else:
                        if tool_name in tools:
                            print(f"Tool '{tool_name}' requires parameters. Try one of the quick tests:")
                            print("  test_connection, get_status, get_users, get_customers, get_products")
                        else:
                            print(f"Unknown tool: {tool_name}")
                        continue
                    
                    print(self.format_response(result))
                
                elif command:
                    print("Unknown command. Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
        # Cleanup
        if self.client:
            self.client.close()
        
        print("\n👋 Goodbye!")


def main():
    """Main entry point."""
    server = UltraSimpleServer("dolibarr-mcp-ultra")
    server.run_interactive()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Server error: {e}", file=sys.stderr)
        sys.exit(1)
