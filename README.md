# Dolibarr MCP Server

Professional Model Context Protocol (MCP) server for comprehensive Dolibarr ERP integration with full CRUD operations and business intelligence capabilities.

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCP Compatible](https://img.shields.io/badge/MCP-1.0.0-orange.svg)](https://modelcontextprotocol.io)

## 🚀 Features

### Complete ERP Management
- **Customer/Third Party Management**: Full CRUD operations for customers and suppliers
- **Product Catalog**: Comprehensive product management with inventory tracking
- **Invoice Management**: Create, update, and track invoices with line items
- **Order Processing**: Complete order lifecycle management
- **Contact Management**: Maintain detailed contact records
- **User Administration**: User account and permissions management

### Professional Grade
- **Asynchronous Operations**: High-performance async/await architecture
- **Error Handling**: Comprehensive error handling with detailed logging
- **Type Safety**: Full type hints with Pydantic validation
- **CLI Interface**: Professional command-line tools for testing and management
- **Raw API Access**: Direct access to any Dolibarr API endpoint

### MCP Integration
- **Tool-based Architecture**: Each operation exposed as an MCP tool
- **Schema Validation**: Proper input/output schema validation
- **Response Formatting**: Structured JSON responses
- **Error Propagation**: Meaningful error messages and status codes

## 📋 Prerequisites

- Python 3.8 or higher
- Dolibarr instance with API enabled
- Dolibarr API key with appropriate permissions

## 🛠️ Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/latinogino/dolibarr-mcp.git
cd dolibarr-mcp

# Install in development mode
pip install -e .

# Or install dependencies directly
pip install -r requirements.txt
```

### Using pip (when published)

```bash
pip install dolibarr-mcp
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in your project directory:

```bash
# Copy the example file
cp .env.example .env
```

Edit the `.env` file with your Dolibarr configuration:

```env
# Dolibarr API Configuration
DOLIBARR_URL=https://your-dolibarr-instance.com/api/index.php
DOLIBARR_API_KEY=your_dolibarr_api_key_here

# Logging Configuration
LOG_LEVEL=INFO
```

### Dolibarr API Setup

1. **Enable the API module** in Dolibarr:
   - Go to Home → Setup → Modules
   - Enable "Web Services API REST (developer)"

2. **Create an API key**:
   - Go to Home → Setup → API/Web services
   - Create a new API key for your user
   - Ensure the user has appropriate permissions

3. **Test the API**:
   ```bash
   curl -X GET "https://your-dolibarr-instance.com/api/index.php/status" \
     -H "DOLAPIKEY: your_api_key_here"
   ```

## 🚀 Usage

### Command Line Interface

Test your connection:
```bash
dolibarr-mcp test
```

Test with specific credentials:
```bash
dolibarr-mcp test --url "https://your-instance.com/api/index.php" --api-key "your_key"
```

Start the MCP server:
```bash
dolibarr-mcp serve
```

### As an MCP Server

The server exposes comprehensive tools for Dolibarr management:

#### System Tools
- `test_connection` - Test API connectivity
- `get_status` - Get system status and version

#### Customer Management
- `get_customers` - List customers/third parties
- `get_customer_by_id` - Get specific customer details
- `create_customer` - Create new customer
- `update_customer` - Update existing customer
- `delete_customer` - Delete customer

#### Product Management  
- `get_products` - List products
- `get_product_by_id` - Get specific product details
- `create_product` - Create new product
- `update_product` - Update existing product
- `delete_product` - Delete product

#### Invoice Management
- `get_invoices` - List invoices
- `get_invoice_by_id` - Get specific invoice details
- `create_invoice` - Create new invoice with line items
- `update_invoice` - Update existing invoice
- `delete_invoice` - Delete invoice

#### Order Management
- `get_orders` - List orders
- `get_order_by_id` - Get specific order details
- `create_order` - Create new order
- `update_order` - Update existing order
- `delete_order` - Delete order

#### Contact Management
- `get_contacts` - List contacts
- `get_contact_by_id` - Get specific contact details
- `create_contact` - Create new contact
- `update_contact` - Update existing contact
- `delete_contact` - Delete contact

#### User Management
- `get_users` - List users
- `get_user_by_id` - Get specific user details
- `create_user` - Create new user
- `update_user` - Update existing user
- `delete_user` - Delete user

#### Raw API Access
- `dolibarr_raw_api` - Make direct API calls to any endpoint

### Programmatic Usage

```python
import asyncio
from dolibarr_mcp import Config, DolibarrClient

async def main():
    config = Config.from_env()
    
    async with DolibarrClient(config) as client:
        # Get customers
        customers = await client.get_customers(limit=10)
        print(f"Found {len(customers)} customers")
        
        # Create a new customer
        new_customer = await client.create_customer(
            name="Test Company",
            email="test@company.com",
            phone="+1-555-0123"
        )
        print(f"Created customer: {new_customer}")
        
        # Get products
        products = await client.get_products(limit=5)
        print(f"Found {len(products)} products")

asyncio.run(main())
```

## 🏗️ Architecture

### Project Structure

```
dolibarr-mcp/
├── src/dolibarr_mcp/
│   ├── __init__.py           # Package exports
│   ├── config.py             # Configuration management
│   ├── cli.py                # Command line interface
│   ├── dolibarr_client.py    # API client implementation
│   └── dolibarr_mcp_server.py # MCP server implementation
├── tests/                    # Test suite
├── api/                      # API documentation
├── pyproject.toml           # Project configuration
├── requirements.txt         # Dependencies
└── README.md               # This file
```

### API Client Architecture

The `DolibarrClient` provides:

- **Async Context Manager**: Proper session management
- **Error Handling**: Custom `DolibarrAPIError` exceptions
- **Request/Response Logging**: Detailed debugging information
- **Type Safety**: Full type hints for all methods
- **Flexible Configuration**: Environment-based configuration

### MCP Server Architecture

The MCP server follows the official MCP specification:

- **Tool Registration**: Each operation is a registered tool
- **Schema Validation**: Input/output validation using JSON schemas
- **Error Propagation**: Meaningful error responses
- **Async Operation**: Non-blocking request handling

## 🧪 Testing

Run the test suite:

```bash
# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=src/dolibarr_mcp
```

Test specific functionality:

```bash
# Test API connection
dolibarr-mcp test

# Test with verbose output
dolibarr-mcp test --verbose
```

## 📝 API Reference

### Configuration

The `Config` class manages all configuration:

```python
from dolibarr_mcp import Config

# From environment variables
config = Config.from_env()

# Manual configuration
config = Config(
    dolibarr_url="https://your-instance.com/api/index.php",
    api_key="your_api_key",
    log_level="DEBUG"
)
```

### Client Usage

```python
from dolibarr_mcp import DolibarrClient, Config

config = Config.from_env()

async with DolibarrClient(config) as client:
    # All operations here
    pass
```

### Error Handling

```python
from dolibarr_mcp import DolibarrAPIError

try:
    result = await client.get_customers()
except DolibarrAPIError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
    print(f"Response Data: {e.response_data}")
```

## 🐳 Docker Support (Coming Soon)

Docker containerization is planned for the second phase of development:

```bash
# Build image
docker build -t dolibarr-mcp .

# Run container
docker run -p 8080:8080 --env-file .env dolibarr-mcp
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/dolibarr-mcp.git
cd dolibarr-mcp

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Dolibarr](https://www.dolibarr.org/) - The amazing open-source ERP/CRM
- [Model Context Protocol](https://modelcontextprotocol.io/) - The protocol specification
- [Anthropic](https://www.anthropic.com/) - For the MCP standard

## 📞 Support

- 📖 [Documentation](https://github.com/latinogino/dolibarr-mcp#readme)
- 🐛 [Issue Tracker](https://github.com/latinogino/dolibarr-mcp/issues)
- 💬 [Discussions](https://github.com/latinogino/dolibarr-mcp/discussions)

## 🗺️ Roadmap

### Phase 1 (Current) ✅
- [x] Core MCP server implementation
- [x] Full CRUD operations for main entities
- [x] Professional error handling
- [x] CLI interface
- [x] Comprehensive documentation

### Phase 2 (Next)
- [ ] Docker containerization
- [ ] Advanced filtering and search
- [ ] Webhook support
- [ ] Performance optimization
- [ ] Extended API coverage

### Phase 3 (Future)
- [ ] Web UI for management
- [ ] Multi-instance support
- [ ] Caching layer
- [ ] Metrics and monitoring
- [ ] Plugin system

---

**Built with ❤️ for the Dolibarr community**
