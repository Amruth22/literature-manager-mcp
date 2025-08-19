#!/usr/bin/env python3
"""
Literature Manager MCP Server

This is the main entry point for the Literature Manager MCP server.
It provides a beginner-friendly interface for managing research literature.
"""

import os
import sys
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.tools import mcp

def main():
    """Main entry point for the MCP server."""
    
    # Check if database path is set
    db_path = os.environ.get('LITERATURE_DB_PATH')
    if not db_path:
        print("❌ Error: LITERATURE_DB_PATH environment variable not set")
        print("\nPlease set the path to your literature database:")
        print("  export LITERATURE_DB_PATH=/path/to/your/literature.db")
        print("\nOr create a new database first:")
        print("  python setup_database.py")
        sys.exit(1)
    
    # Check if database exists
    if not Path(db_path).exists():
        print(f"❌ Error: Database not found at {db_path}")
        print("\nPlease create the database first:")
        print("  python setup_database.py")
        sys.exit(1)
    
    print("🚀 Starting Literature Manager MCP Server...")
    print(f"📚 Database: {db_path}")
    print("✅ Server ready for connections!")
    
    # Start the FastMCP server
    mcp.run()

if __name__ == "__main__":
    main()