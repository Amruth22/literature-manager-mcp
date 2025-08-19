#!/usr/bin/env python3
"""
Database Setup Script for Literature Manager

This script creates the SQLite database with all necessary tables.
Run this once before using the literature manager.
"""

import sqlite3
import os
from pathlib import Path

def create_database(db_path: str = "literature.db"):
    """
    Create the literature management database with all required tables.
    
    Args:
        db_path: Path where to create the database file
    """
    
    # Convert to Path object for better handling
    db_path = Path(db_path)
    
    # Check if database already exists
    if db_path.exists():
        response = input(f"Database {db_path} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
        db_path.unlink()  # Delete existing database
    
    print(f"Creating database at: {db_path.absolute()}")
    
    # Create database and tables
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create sources table
        print("Creating sources table...")
        cursor.execute("""
            CREATE TABLE sources (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                type TEXT CHECK(type IN ('paper', 'webpage', 'book', 'video', 'blog')) NOT NULL,
                identifiers TEXT NOT NULL,
                status TEXT CHECK(status IN ('unread', 'reading', 'completed', 'archived')) DEFAULT 'unread',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create source notes table
        print("Creating source_notes table...")
        cursor.execute("""
            CREATE TABLE source_notes (
                source_id TEXT REFERENCES sources(id),
                note_title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (source_id, note_title)
            )
        """)
        
        # Create entity links table
        print("Creating source_entity_links table...")
        cursor.execute("""
            CREATE TABLE source_entity_links (
                source_id TEXT REFERENCES sources(id),
                entity_name TEXT,
                relation_type TEXT CHECK(relation_type IN ('discusses', 'introduces', 'extends', 'evaluates', 'applies', 'critiques')),
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (source_id, entity_name)
            )
        """)
        
        # Create indexes for better performance
        print("Creating indexes...")
        cursor.execute("CREATE INDEX idx_sources_type ON sources(type)")
        cursor.execute("CREATE INDEX idx_sources_status ON sources(status)")
        cursor.execute("CREATE INDEX idx_sources_created ON sources(created_at)")
        cursor.execute("CREATE INDEX idx_source_notes_created ON source_notes(created_at)")
        cursor.execute("CREATE INDEX idx_entity_links_name ON source_entity_links(entity_name)")
        cursor.execute("CREATE INDEX idx_entity_links_created ON source_entity_links(created_at)")
        
        conn.commit()
        print("✅ Database created successfully!")
        
        # Show table info
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"\nCreated {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
    
    print(f"\n🎉 Setup complete! Your database is ready at: {db_path.absolute()}")
    print("\nNext steps:")
    print("1. Set the LITERATURE_DB_PATH environment variable:")
    print(f"   export LITERATURE_DB_PATH='{db_path.absolute()}'")
    print("2. Run the MCP server:")
    print("   python server.py")
    print("3. Or configure it in Claude Desktop (see README.md)")

def main():
    """Main setup function with user interaction."""
    print("📚 Literature Manager Database Setup")
    print("=" * 40)
    
    # Get database path from user
    default_path = "literature.db"
    db_path = input(f"Database path (default: {default_path}): ").strip()
    if not db_path:
        db_path = default_path
    
    try:
        create_database(db_path)
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())