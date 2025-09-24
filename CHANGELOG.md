# Changelog

All notable changes to the Dolibarr MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-09-24

### 🔥 MAJOR FIX: Windows Compatibility
- **FIXED**: Windows pywin32 permission issues that prevented installation
- **ADDED**: Standalone server implementation that works WITHOUT MCP package
- **ADDED**: `setup_standalone.bat` - Windows-optimized setup script  
- **ADDED**: `run_standalone.bat` - Start standalone server
- **ADDED**: `requirements-windows.txt` - pywin32-free dependencies
- **ADDED**: `test_standalone.py` - Test script for standalone version

### ✨ New Features
- **ADDED**: Interactive testing mode in standalone server
- **ADDED**: Enhanced error handling with detailed API error messages
- **ADDED**: Professional configuration validation with helpful setup guides
- **ADDED**: Comprehensive German README (`README_DE.md`)

### 🛠️ Improvements
- **IMPROVED**: Setup process with multiple fallback options
- **IMPROVED**: Error messages with actionable troubleshooting steps
- **IMPROVED**: Documentation with Windows-specific troubleshooting
- **IMPROVED**: Docker configuration with health checks and resource limits

### 📋 Available Tools (Complete CRUD for all modules)
- ✅ **System**: `test_connection`, `get_status`
- ✅ **Users**: `get_users`, `get_user_by_id`, `create_user`, `update_user`, `delete_user`
- ✅ **Customers**: `get_customers`, `get_customer_by_id`, `create_customer`, `update_customer`, `delete_customer` 
- ✅ **Products**: `get_products`, `get_product_by_id`, `create_product`, `update_product`, `delete_product`
- ✅ **Invoices**: `get_invoices`, `get_invoice_by_id`, `create_invoice`, `update_invoice`, `delete_invoice`
- ✅ **Orders**: `get_orders`, `get_order_by_id`, `create_order`, `update_order`, `delete_order`
- ✅ **Contacts**: `get_contacts`, `get_contact_by_id`, `create_contact`, `update_contact`, `delete_contact`
- ✅ **Raw API**: `dolibarr_raw_api` - Direct access to any Dolibarr endpoint

### 🐳 Docker
- **ADDED**: Multi-stage Dockerfile for optimized production builds
- **ADDED**: docker-compose.yml with health checks
- **ADDED**: Test service configuration for automated testing

### 📚 Documentation  
- **ADDED**: Comprehensive setup instructions for Windows
- **ADDED**: Troubleshooting guide for common issues
- **ADDED**: API endpoint documentation and examples
- **ADDED**: Contributing guidelines

## [1.0.1] - 2025-09-23

### Initial Release
- **ADDED**: Complete Dolibarr API client with async/await
- **ADDED**: MCP server implementation with 30+ tools
- **ADDED**: Professional error handling and logging
- **ADDED**: Docker support with production configuration
- **ADDED**: Comprehensive test suite
- **ADDED**: Configuration management with .env support

### Core Features
- Full CRUD operations for all major Dolibarr modules
- Async HTTP client with proper connection handling  
- Pydantic validation for type safety
- Professional logging and error reporting
- MCP 1.0 compliance for LLM integration

### Supported Dolibarr Modules
- User Management
- Customer/Third Party Management  
- Product Management
- Invoice Management
- Order Management
- Contact Management
- Raw API access for extensibility

---

## Installation Summary

### Windows Users (RECOMMENDED)
```cmd
.\setup_standalone.bat  # Avoids pywin32 issues
.\run_standalone.bat    # Start server
```

### Linux/macOS Users  
```bash
./setup.sh
python -m src.dolibarr_mcp
```

### Docker Users
```bash
docker-compose up -d
```

## Support

- 🐛 Issues: [GitHub Issues](https://github.com/latinogino/dolibarr-mcp/issues)
- 💡 Discussions: [GitHub Discussions](https://github.com/latinogino/dolibarr-mcp/discussions)
- 📖 Wiki: [Project Wiki](https://github.com/latinogino/dolibarr-mcp/wiki)
