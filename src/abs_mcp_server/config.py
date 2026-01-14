"""Centralized configuration for ABS MCP Server."""
import os
from pathlib import Path

class Config:
    """Configuration settings for the ABS MCP Server and Client."""
    
    # ABS API Settings
    ABS_API_BASE = os.getenv("ABS_API_BASE", "https://api.data.abs.gov.au")
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))  # seconds
    
    # Agent Settings (Client)
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.0-flash")  # Stable production model
    
    # Data Settings
    MAX_OBSERVATIONS = int(os.getenv("MAX_OBSERVATIONS", "50"))
    
    # Logging Settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    TRACE_FILE = Path(os.getenv("TRACE_FILE", "query_trace.jsonl"))
    ENABLE_TRACING = os.getenv("ENABLE_TRACING", "true").lower() == "true"
    
    # Performance Settings
    ENABLE_CACHING = os.getenv("ENABLE_CACHING", "true").lower() == "true"
    CACHE_SIZE = int(os.getenv("CACHE_SIZE", "100"))
    
    # Safety Settings
    MAX_TURNS = int(os.getenv("MAX_TURNS", "5"))  # Max LLM invocations per query
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
    
    @classmethod
    def __repr__(cls) -> str:
        """Return configuration summary (sanitized)."""
        return f"""Config(
    ABS_API_BASE={cls.ABS_API_BASE},
    LLM_MODEL={cls.LLM_MODEL},
    MAX_OBSERVATIONS={cls.MAX_OBSERVATIONS},
    ENABLE_CACHING={cls.ENABLE_CACHING}
)"""
