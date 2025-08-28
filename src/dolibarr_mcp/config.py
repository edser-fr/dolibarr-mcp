"""Configuration management for Dolibarr MCP Server."""

import os
from typing import Optional

from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config(BaseModel):
    """Configuration for Dolibarr MCP Server."""
    
    dolibarr_url: str = Field(
        description="Dolibarr API URL",
        default_factory=lambda: os.getenv("DOLIBARR_URL", "")
    )
    
    api_key: str = Field(
        description="Dolibarr API key",
        default_factory=lambda: os.getenv("DOLIBARR_API_KEY", "")
    )
    
    log_level: str = Field(
        description="Logging level",
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO")
    )
    
    @validator('dolibarr_url')
    def validate_dolibarr_url(cls, v):
        """Validate Dolibarr URL."""
        if not v:
            raise ValueError("DOLIBARR_URL environment variable is required")
        
        if not v.startswith(('http://', 'https://')):
            raise ValueError("DOLIBARR_URL must start with http:// or https://")
        
        # Ensure it ends with the proper API path
        if not v.endswith('/api/index.php'):
            if v.endswith('/'):
                v = v + 'api/index.php'
            else:
                v = v + '/api/index.php'
                
        return v
    
    @validator('api_key')
    def validate_api_key(cls, v):
        """Validate API key."""
        if not v:
            raise ValueError(
                "DOLIBARR_API_KEY environment variable is required. "
                "Please create an API key in Dolibarr at: Home → Setup → API/Web services"
            )
        
        if len(v) < 10:
            raise ValueError("DOLIBARR_API_KEY appears to be too short. Please check your API key.")
            
        return v
    
    @validator('log_level')
    def validate_log_level(cls, v):
        """Validate log level."""
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        if v.upper() not in valid_levels:
            raise ValueError(f"LOG_LEVEL must be one of: {', '.join(valid_levels)}")
        return v.upper()
    
    @classmethod
    def from_env(cls) -> "Config":
        """Create configuration from environment variables with validation."""
        try:
            return cls()
        except Exception as e:
            print(f"❌ Configuration Error: {e}")
            print()
            print("💡 Quick Setup Guide:")
            print("1. Copy .env.example to .env")
            print("2. Edit .env with your Dolibarr details:")
            print("   DOLIBARR_URL=https://your-dolibarr-instance.com")
            print("   DOLIBARR_API_KEY=your_api_key_here")
            print()
            print("🔧 Dolibarr API Key Setup:")
            print("   1. Login to Dolibarr as admin")
            print("   2. Go to: Home → Setup → Modules")
            print("   3. Enable: 'Web Services API REST (developer)'")
            print("   4. Go to: Home → Setup → API/Web services")
            print("   5. Create a new API key")
            print()
            raise
    
    class Config:
        """Pydantic config."""
        env_file = '.env'
        env_file_encoding = 'utf-8'
