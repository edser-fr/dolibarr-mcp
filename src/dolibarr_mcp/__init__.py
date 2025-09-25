"""Dolibarr MCP - Model Context Protocol Server for Dolibarr ERP."""

__version__ = "1.0.1"
__author__ = "Dolibarr MCP Team"

# Make the main function available at package level
try:
    from .dolibarr_mcp_server import main
except ImportError:
    # If relative import fails, we might be running directly
    import sys
    import os
    # Add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from dolibarr_mcp.dolibarr_mcp_server import main

# Export main components
__all__ = [
    'main',
    '__version__',
    '__author__'
]

# Support both execution methods
if __name__ == '__main__':
    main()
