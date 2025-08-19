#!/usr/bin/env python3
"""
Basic Usage Examples for Literature Manager

This file shows simple examples of how to use the literature manager
through the MCP interface or directly with the database classes.
"""

import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.database import LiteratureDatabase, DatabaseError

def setup_example_database():
    """Create an example database with sample data."""
    
    # Use a test database
    db_path = "example_literature.db"
    
    # Remove existing database
    if Path(db_path).exists():
        Path(db_path).unlink()
    
    # Create database (you would normally run setup_database.py)
    import sqlite3
    import json
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create tables (simplified version)
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
        
        cursor.execute("""
            CREATE TABLE source_notes (
                source_id TEXT REFERENCES sources(id),
                note_title TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (source_id, note_title)
            )
        """)
        
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
        
        conn.commit()
    
    return db_path

def example_1_add_sources():
    """Example 1: Adding different types of sources."""
    
    print("📚 Example 1: Adding Sources")
    print("=" * 40)
    
    db_path = setup_example_database()
    db = LiteratureDatabase(db_path)
    
    try:
        # Add a research paper
        print("Adding research paper...")
        paper_id = db.add_source(
            title="Attention Is All You Need",
            source_type="paper",
            identifier_type="arxiv",
            identifier_value="1706.03762"
        )
        print(f"✅ Added paper with ID: {paper_id}")
        
        # Add a book
        print("\nAdding book...")
        book_id = db.add_source(
            title="Deep Learning",
            source_type="book",
            identifier_type="isbn",
            identifier_value="978-0262035613"
        )
        print(f"✅ Added book with ID: {book_id}")
        
        # Add a webpage
        print("\nAdding webpage...")
        webpage_id = db.add_source(
            title="The Illustrated Transformer",
            source_type="webpage",
            identifier_type="url",
            identifier_value="https://jalammar.github.io/illustrated-transformer/"
        )
        print(f"✅ Added webpage with ID: {webpage_id}")
        
        return db, [paper_id, book_id, webpage_id]
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")
        return None, []

def example_2_add_notes(db, source_ids):
    """Example 2: Adding notes to sources."""
    
    print("\n📝 Example 2: Adding Notes")
    print("=" * 40)
    
    if not db or not source_ids:
        print("❌ No sources available from previous example")
        return
    
    try:
        # Add note to the paper
        print("Adding note to research paper...")
        db.add_note(
            source_ids[0],  # paper ID
            "Key Innovation",
            "The transformer architecture eliminates the need for recurrence and convolutions, "
            "relying entirely on attention mechanisms."
        )
        print("✅ Added note to paper")
        
        # Add note to the book
        print("\nAdding note to book...")
        db.add_note(
            source_ids[1],  # book ID
            "Overview",
            "Comprehensive textbook covering deep learning from basics to advanced topics. "
            "Great for both beginners and researchers."
        )
        print("✅ Added note to book")
        
        # Add multiple notes to webpage
        print("\nAdding multiple notes to webpage...")
        db.add_note(
            source_ids[2],  # webpage ID
            "Visual Explanation",
            "Excellent visual explanation of transformer architecture with step-by-step illustrations."
        )
        db.add_note(
            source_ids[2],  # webpage ID
            "Accessibility",
            "Makes complex concepts accessible to beginners through clear visualizations."
        )
        print("✅ Added multiple notes to webpage")
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")

def example_3_update_status(db, source_ids):
    """Example 3: Updating reading status."""
    
    print("\n📊 Example 3: Updating Status")
    print("=" * 40)
    
    if not db or not source_ids:
        print("❌ No sources available from previous example")
        return
    
    try:
        # Update paper status to completed
        print("Marking paper as completed...")
        db.update_status(source_ids[0], "completed")
        print("✅ Paper marked as completed")
        
        # Update book status to reading
        print("\nMarking book as currently reading...")
        db.update_status(source_ids[1], "reading")
        print("✅ Book marked as reading")
        
        # Keep webpage as unread (default)
        print("\nWebpage remains unread (default status)")
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")

def example_4_entity_links(db, source_ids):
    """Example 4: Linking sources to entities."""
    
    print("\n🔗 Example 4: Entity Links")
    print("=" * 40)
    
    if not db or not source_ids:
        print("❌ No sources available from previous example")
        return
    
    try:
        # Link paper to transformer concept
        print("Linking paper to 'transformer architecture'...")
        db.link_to_entity(
            source_ids[0],  # paper ID
            "transformer architecture",
            "introduces",
            "First paper to introduce the transformer model architecture"
        )
        print("✅ Linked paper to transformer architecture")
        
        # Link book to deep learning concept
        print("\nLinking book to 'deep learning'...")
        db.link_to_entity(
            source_ids[1],  # book ID
            "deep learning",
            "discusses",
            "Comprehensive coverage of deep learning concepts and techniques"
        )
        print("✅ Linked book to deep learning")
        
        # Link webpage to both concepts
        print("\nLinking webpage to multiple concepts...")
        db.link_to_entity(
            source_ids[2],  # webpage ID
            "transformer architecture",
            "explains",
            "Visual explanation of how transformers work"
        )
        db.link_to_entity(
            source_ids[2],  # webpage ID
            "attention mechanism",
            "discusses",
            "Detailed explanation of attention mechanisms in transformers"
        )
        print("✅ Linked webpage to multiple concepts")
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")

def example_5_retrieve_data(db, source_ids):
    """Example 5: Retrieving and displaying data."""
    
    print("\n📖 Example 5: Retrieving Data")
    print("=" * 40)
    
    if not db or not source_ids:
        print("❌ No sources available from previous example")
        return
    
    try:
        # Get complete source details
        print("Getting complete details for all sources...")
        
        for i, source_id in enumerate(source_ids):
            source = db.get_source_by_id(source_id)
            if source:
                print(f"\n--- Source {i+1}: {source['title']} ---")
                print(f"Type: {source['type']}")
                print(f"Status: {source['status']}")
                print(f"Identifiers: {source['identifiers']}")
                
                if source['notes']:
                    print(f"Notes ({len(source['notes'])}):")
                    for note in source['notes']:
                        print(f"  • {note['title']}: {note['content'][:50]}...")
                
                if source['entity_links']:
                    print(f"Entity Links ({len(source['entity_links'])}):")
                    for link in source['entity_links']:
                        print(f"  • {link['entity_name']} ({link['relation_type']})")
        
        # Show database statistics
        print("\n--- Database Statistics ---")
        stats = db.get_database_stats()
        print(f"Total Sources: {stats['total_sources']}")
        print(f"Total Notes: {stats['total_notes']}")
        print(f"Total Entity Links: {stats['total_entity_links']}")
        
        if stats['sources_by_type']:
            print("Sources by Type:")
            for source_type, count in stats['sources_by_type'].items():
                print(f"  {source_type}: {count}")
        
        if stats['sources_by_status']:
            print("Sources by Status:")
            for status, count in stats['sources_by_status'].items():
                print(f"  {status}: {count}")
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")

def main():
    """Run all examples."""
    
    print("🚀 Literature Manager - Basic Usage Examples")
    print("=" * 50)
    
    # Run examples in sequence
    db, source_ids = example_1_add_sources()
    
    if db and source_ids:
        example_2_add_notes(db, source_ids)
        example_3_update_status(db, source_ids)
        example_4_entity_links(db, source_ids)
        example_5_retrieve_data(db, source_ids)
    
    print("\n🎉 Examples completed!")
    print("\nNext steps:")
    print("1. Run 'python setup_database.py' to create your own database")
    print("2. Set LITERATURE_DB_PATH environment variable")
    print("3. Run 'python server.py' to start the MCP server")
    print("4. Configure Claude Desktop to use the server")

if __name__ == "__main__":
    main()