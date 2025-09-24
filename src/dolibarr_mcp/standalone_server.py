"""Standalone Dolibarr MCP Server - Windows Compatible (No pywin32 needed)."""

import asyncio
import json
import sys
import os
import logging
from typing import Any, Dict, List, Optional, Union

# Standard library only - no MCP package needed
from contextlib import asynccontextmanager

# Our Dolibarr components
from .config import Config
from .dolibarr_client import DolibarrClient, DolibarrAPIError

# Configure logging to stderr
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)]
)

class StandaloneMCPServer:
    """Standalone MCP Server implementation without pywin32 dependencies."""
    
    def __init__(self, name: str = "dolibarr-mcp"):
        self.name = name
        self.logger = logging.getLogger(__name__)
        
    def get_tool_definitions(self) -> List[Dict[str, Any]]:
        """Get all available tool definitions."""
        return [
            # System & Info
            {
                "name": "test_connection",
                "description": "Test Dolibarr API connection",
                "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}
            },
            {
                "name": "get_status",
                "description": "Get Dolibarr system status and version information",
                "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False}
            },
            
            # User Management CRUD
            {
                "name": "get_users",
                "description": "Get list of users from Dolibarr",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Maximum number of users to return (default: 100)", "default": 100},
                        "page": {"type": "integer", "description": "Page number for pagination (default: 1)", "default": 1}
                    },
                    "additionalProperties": False
                }
            },
            {
                "name": "get_user_by_id",
                "description": "Get specific user details by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "User ID to retrieve"}
                    },
                    "required": ["user_id"],
                    "additionalProperties": False
                }
            },
            {
                "name": "create_user",
                "description": "Create a new user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "login": {"type": "string", "description": "User login"},
                        "lastname": {"type": "string", "description": "Last name"},
                        "firstname": {"type": "string", "description": "First name"},
                        "email": {"type": "string", "description": "Email address"},
                        "password": {"type": "string", "description": "Password"},
                        "admin": {"type": "integer", "description": "Admin level (0=No, 1=Yes)", "default": 0}
                    },
                    "required": ["login", "lastname"],
                    "additionalProperties": False
                }
            },
            {
                "name": "update_user",
                "description": "Update an existing user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "User ID to update"},
                        "login": {"type": "string", "description": "User login"},
                        "lastname": {"type": "string", "description": "Last name"},
                        "firstname": {"type": "string", "description": "First name"},
                        "email": {"type": "string", "description": "Email address"},
                        "admin": {"type": "integer", "description": "Admin level (0=No, 1=Yes)"}
                    },
                    "required": ["user_id"],
                    "additionalProperties": False
                }
            },
            {
                "name": "delete_user",
                "description": "Delete a user",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "integer", "description": "User ID to delete"}
                    },
                    "required": ["user_id"],
                    "additionalProperties": False
                }
            },
            
            # Customer/Third Party Management CRUD
            {
                "name": "get_customers",
                "description": "Get list of customers/third parties from Dolibarr",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Maximum number of customers to return (default: 100)", "default": 100},
                        "page": {"type": "integer", "description": "Page number for pagination (default: 1)", "default": 1}
                    },
                    "additionalProperties": False
                }
            },
            {
                "name": "get_customer_by_id",
                "description": "Get specific customer details by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "integer", "description": "Customer ID to retrieve"}
                    },
                    "required": ["customer_id"],
                    "additionalProperties": False
                }
            },
            {
                "name": "create_customer",
                "description": "Create a new customer/third party",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Customer name"},
                        "email": {"type": "string", "description": "Email address"},
                        "phone": {"type": "string", "description": "Phone number"},
                        "address": {"type": "string", "description": "Customer address"},
                        "town": {"type": "string", "description": "City/Town"},
                        "zip": {"type": "string", "description": "Postal code"},
                        "country_id": {"type": "integer", "description": "Country ID (default: 1)", "default": 1},
                        "type": {"type": "integer", "description": "Customer type (1=Customer, 2=Supplier, 3=Both)", "default": 1},
                        "status": {"type": "integer", "description": "Status (1=Active, 0=Inactive)", "default": 1}
                    },
                    "required": ["name"],
                    "additionalProperties": False
                }
            },
            {
                "name": "update_customer",
                "description": "Update an existing customer",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "integer", "description": "Customer ID to update"},
                        "name": {"type": "string", "description": "Customer name"},
                        "email": {"type": "string", "description": "Email address"},
                        "phone": {"type": "string", "description": "Phone number"},
                        "address": {"type": "string", "description": "Customer address"},
                        "town": {"type": "string", "description": "City/Town"},
                        "zip": {"type": "string", "description": "Postal code"},
                        "status": {"type": "integer", "description": "Status (1=Active, 0=Inactive)"}
                    },
                    "required": ["customer_id"],
                    "additionalProperties": False
                }
            },
            {
                "name": "delete_customer",
                "description": "Delete a customer",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "customer_id": {"type": "integer", "description": "Customer ID to delete"}
                    },
                    "required": ["customer_id"],
                    "additionalProperties": False
                }
            },
            
            # Product Management CRUD
            {
                "name": "get_products",
                "description": "Get list of products from Dolibarr",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "description": "Maximum number of products to return (default: 100)", "default": 100}
                    },
                    "additionalProperties": False
                }
            },
            {
                "name": "get_product_by_id",
                "description": "Get specific product details by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "integer", "description": "Product ID to retrieve"}
                    },
                    "required": ["product_id"],
                    "additionalProperties": False
                }
            },
            {
                "name": "create_product",
                "description": "Create a new product",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "label": {"type": "string", "description": "Product name/label"},
                        "price": {"type": "number", "description": "Product price"},
                        "description": {"type": "string", "description": "Product description"},
                        "stock": {"type": "integer", "description": "Initial stock quantity"}
                    },
                    "required": ["label", "price"],
                    "additionalProperties": False
                }
            },
            {
                "name": "update_product",
                "description": "Update an existing product",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "integer", "description": "Product ID to update"},
                        "label": {"type": "string", "description": "Product name/label"},
                        "price": {"type": "number", "description": "Product price"},
                        "description": {"type": "string", "description": "Product description"}
                    },
                    "required": ["product_id"],
                    "additionalProperties": False
                }
            },
            {
                "name": "delete_product",
                "description": "Delete a product",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "product_id": {"type": "integer", "description": "Product ID to delete"}
                    },
                    "required": ["product_id"],
                    "additionalProperties": False
                }
            },
            
            # Raw API Access
            {
                "name": "dolibarr_raw_api",
                "description": "Make raw API call to any Dolibarr endpoint",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "method": {"type": "string", "description": "HTTP method", "enum": ["GET", "POST", "PUT", "DELETE"]},
                        "endpoint": {"type": "string", "description": "API endpoint (e.g., /thirdparties, /invoices)"},
                        "params": {"type": "object", "description": "Query parameters"},
                        "data": {"type": "object", "description": "Request payload for POST/PUT requests"}
                    },
                    "required": ["method", "endpoint"],
                    "additionalProperties": False
                }
            }
        ]
    
    async def handle_tool_call(self, name: str, arguments: dict) -> Dict[str, Any]:
        """Handle tool calls using the DolibarrClient."""
        
        try:
            # Initialize the config and client
            config = Config()
            
            async with DolibarrClient(config) as client:
                
                # System & Info
                if name == "test_connection":
                    result = await client.get_status()
                    if 'success' not in result:
                        result = {"status": "success", "message": "API connection working", "data": result}
                
                elif name == "get_status":
                    result = await client.get_status()
                
                # User Management
                elif name == "get_users":
                    result = await client.get_users(
                        limit=arguments.get('limit', 100),
                        page=arguments.get('page', 1)
                    )
                
                elif name == "get_user_by_id":
                    result = await client.get_user_by_id(arguments['user_id'])
                
                elif name == "create_user":
                    result = await client.create_user(**arguments)
                
                elif name == "update_user":
                    user_id = arguments.pop('user_id')
                    result = await client.update_user(user_id, **arguments)
                
                elif name == "delete_user":
                    result = await client.delete_user(arguments['user_id'])
                
                # Customer Management
                elif name == "get_customers":
                    result = await client.get_customers(
                        limit=arguments.get('limit', 100),
                        page=arguments.get('page', 1)
                    )
                
                elif name == "get_customer_by_id":
                    result = await client.get_customer_by_id(arguments['customer_id'])
                
                elif name == "create_customer":
                    result = await client.create_customer(**arguments)
                
                elif name == "update_customer":
                    customer_id = arguments.pop('customer_id')
                    result = await client.update_customer(customer_id, **arguments)
                
                elif name == "delete_customer":
                    result = await client.delete_customer(arguments['customer_id'])
                
                # Product Management
                elif name == "get_products":
                    result = await client.get_products(limit=arguments.get('limit', 100))
                
                elif name == "get_product_by_id":
                    result = await client.get_product_by_id(arguments['product_id'])
                
                elif name == "create_product":
                    result = await client.create_product(**arguments)
                
                elif name == "update_product":
                    product_id = arguments.pop('product_id')
                    result = await client.update_product(product_id, **arguments)
                
                elif name == "delete_product":
                    result = await client.delete_product(arguments['product_id'])
                
                # Raw API Access
                elif name == "dolibarr_raw_api":
                    result = await client.dolibarr_raw_api(**arguments)
                
                else:
                    result = {"error": f"Unknown tool: {name}"}
            
            return {"success": True, "data": result}
        
        except DolibarrAPIError as e:
            return {"error": f"Dolibarr API Error: {str(e)}", "type": "api_error"}
        
        except Exception as e:
            self.logger.error(f"Tool execution error: {e}")
            return {"error": f"Tool execution failed: {str(e)}", "type": "internal_error"}
    
    def format_response(self, content: Dict[str, Any]) -> str:
        """Format response as JSON string."""
        return json.dumps(content, indent=2, ensure_ascii=False)
    
    async def run_interactive(self):
        """Run server in interactive mode for testing."""
        print("🚀 Standalone Dolibarr MCP Server (Windows Compatible)", file=sys.stderr)
        print("✅ NO pywin32 dependencies required!", file=sys.stderr)
        print("", file=sys.stderr)
        
        # Test API connection
        try:
            config = Config()
            
            if not config.dolibarr_url or config.dolibarr_url.startswith("https://your-dolibarr-instance"):
                print("⚠️  DOLIBARR_URL not configured in .env file", file=sys.stderr)
                print("📝 Please edit .env with your Dolibarr credentials", file=sys.stderr)
            elif not config.api_key or config.api_key in ["your_dolibarr_api_key_here", "placeholder_api_key"]:
                print("⚠️  DOLIBARR_API_KEY not configured in .env file", file=sys.stderr)
                print("📝 Please edit .env with your Dolibarr API key", file=sys.stderr)
            else:
                print("🧪 Testing Dolibarr API connection...", file=sys.stderr)
                test_result = await self.handle_tool_call("test_connection", {})
                if test_result.get("success"):
                    print("✅ Dolibarr API connection successful!", file=sys.stderr)
                else:
                    print(f"⚠️  API test result: {test_result}", file=sys.stderr)
                    
        except Exception as e:
            print(f"⚠️  Configuration error: {e}", file=sys.stderr)
        
        print("", file=sys.stderr)
        print("📋 Available Tools:", file=sys.stderr)
        tools = self.get_tool_definitions()
        for tool in tools:
            print(f"  • {tool['name']} - {tool['description']}", file=sys.stderr)
        
        print("", file=sys.stderr)
        print("💡 Interactive Testing Mode:", file=sys.stderr)
        print("   Type 'list' to see all tools", file=sys.stderr)
        print("   Type 'test <tool_name>' to test a tool", file=sys.stderr)
        print("   Type 'exit' to quit", file=sys.stderr)
        print("", file=sys.stderr)
        
        while True:
            try:
                command = input("dolibarr-mcp> ").strip()
                
                if command == "exit":
                    break
                elif command == "list":
                    print("Available tools:")
                    for tool in tools:
                        print(f"  {tool['name']} - {tool['description']}")
                elif command.startswith("test "):
                    tool_name = command[5:].strip()
                    if tool_name == "test_connection":
                        result = await self.handle_tool_call("test_connection", {})
                        print(self.format_response(result))
                    elif tool_name == "get_status":
                        result = await self.handle_tool_call("get_status", {})
                        print(self.format_response(result))
                    elif tool_name == "get_users":
                        result = await self.handle_tool_call("get_users", {"limit": 5})
                        print(self.format_response(result))
                    elif tool_name == "get_customers":
                        result = await self.handle_tool_call("get_customers", {"limit": 5})
                        print(self.format_response(result))
                    elif tool_name == "get_products":
                        result = await self.handle_tool_call("get_products", {"limit": 5})
                        print(self.format_response(result))
                    else:
                        print(f"Tool '{tool_name}' requires parameters. Available quick tests: test_connection, get_status, get_users, get_customers, get_products")
                elif command:
                    print("Unknown command. Use 'list', 'test <tool_name>', or 'exit'")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
        
        print("\n👋 Goodbye!")


async def main():
    """Main entry point."""
    server = StandaloneMCPServer("dolibarr-mcp-standalone")
    await server.run_interactive()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"❌ Server error: {e}", file=sys.stderr)
        sys.exit(1)
