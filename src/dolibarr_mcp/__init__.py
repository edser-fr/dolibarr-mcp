"""Professional Dolibarr MCP Server package.

This package provides a comprehensive Model Context Protocol (MCP) server
for Dolibarr ERP integration with full CRUD operations.
"""

__version__ = "1.0.0"
__author__ = "Dolibarr MCP Team"
__email__ = "support@dolibarr-mcp.com"

from .config import Config
from .dolibarr_client import DolibarrClient, DolibarrAPIError

__all__ = [
    "Config",
    "DolibarrClient", 
    "DolibarrAPIError",
    "__version__"
]
