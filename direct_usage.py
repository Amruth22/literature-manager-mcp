#!/usr/bin/env python3
"""
Direct Python Usage Example

This script shows how to use the Literature Manager directly in Python
without any MCP client. Perfect for automation, scripts, or Jupyter notebooks.
"""

import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.database import LiteratureDatabase, DatabaseError
from src.utils import format_source_summary

def setup_example():
    """Set up example database and return database instance."""
    
    # Create example database
    db_path = "direct_usage_example.db"
    
    # Remove existing database
    if Path(db_path).exists():
        Path(db_path).unlink()
    
    # Create database schema
    import sqlite3
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
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
    
    return LiteratureDatabase(db_path)

def example_basic_usage():
    """Show basic usage patterns."""
    
    print("📚 Direct Python Usage Examples")
    print("=" * 50)
    
    # Initialize database
    db = setup_example()
    
    print("✅ Database created and initialized")
    
    # Example 1: Add sources
    print("\n1️⃣ Adding Sources")
    print("-" * 20)
    
    try:
        # Add a research paper
        paper_id = db.add_source(
            title="Attention Is All You Need",
            source_type="paper",
            identifier_type="arxiv",
            identifier_value="1706.03762"
        )
        print(f"✅ Added paper: {paper_id}")
        
        # Add a book
        book_id = db.add_source(
            title="Deep Learning",
            source_type="book",
            identifier_type="isbn",
            identifier_value="978-0262035613"
        )
        print(f"✅ Added book: {book_id}")
        
        # Add a webpage
        webpage_id = db.add_source(
            title="The Illustrated Transformer",
            source_type="webpage",
            identifier_type="url",
            identifier_value="https://jalammar.github.io/illustrated-transformer/"
        )
        print(f"✅ Added webpage: {webpage_id}")
        
    except DatabaseError as e:
        print(f"❌ Error adding sources: {e}")
        return
    
    # Example 2: Add notes
    print("\n2️⃣ Adding Notes")
    print("-" * 20)
    
    try:
        # Add notes to the paper
        db.add_note(paper_id, "Key Innovation", 
                   "Introduces the transformer architecture, eliminating recurrence and convolutions")
        db.add_note(paper_id, "Impact", 
                   "Became the foundation for GPT, BERT, and most modern NLP models")
        print("✅ Added notes to paper")
        
        # Add note to book
        db.add_note(book_id, "Overview", 
                   "Comprehensive textbook covering deep learning from basics to advanced topics")
        print("✅ Added note to book")
        
    except DatabaseError as e:
        print(f"❌ Error adding notes: {e}")
    
    # Example 3: Update status
    print("\n3️⃣ Updating Status")
    print("-" * 20)
    
    try:
        # Mark paper as completed
        db.update_status(paper_id, "completed")
        print("✅ Marked paper as completed")
        
        # Mark book as reading
        db.update_status(book_id, "reading")
        print("✅ Marked book as reading")
        
    except DatabaseError as e:
        print(f"❌ Error updating status: {e}")
    
    # Example 4: Link to entities
    print("\n4️⃣ Linking to Entities")
    print("-" * 20)
    
    try:
        # Link paper to transformer concept
        db.link_to_entity(paper_id, "transformer architecture", "introduces",
                         "First paper to introduce the transformer model")
        print("✅ Linked paper to transformer architecture")
        
        # Link book to deep learning concept
        db.link_to_entity(book_id, "deep learning", "discusses",
                         "Comprehensive coverage of deep learning concepts")
        print("✅ Linked book to deep learning")
        
        # Link webpage to transformer concept
        db.link_to_entity(webpage_id, "transformer architecture", "explains",
                         "Visual explanation of how transformers work")
        print("✅ Linked webpage to transformer architecture")
        
    except DatabaseError as e:
        print(f"❌ Error linking entities: {e}")
    
    # Example 5: Retrieve and display data
    print("\n5️⃣ Retrieving Data")
    print("-" * 20)
    
    try:
        # Get detailed source information
        paper = db.get_source_by_id(paper_id)
        print("\n📄 Paper Details:")
        print(format_source_summary(paper))
        
        # List all sources
        all_sources = db.list_sources()
        print(f"\n📚 Total sources in database: {len(all_sources)}")
        
        # Get database statistics
        stats = db.get_database_stats()
        print(f"\n📊 Database Stats:")
        print(f"   Sources: {stats['total_sources']}")
        print(f"   Notes: {stats['total_notes']}")
        print(f"   Entity Links: {stats['total_entity_links']}")
        
    except DatabaseError as e:
        print(f"❌ Error retrieving data: {e}")
    
    return db

def example_automation_script():
    """Show how to use for automation/batch processing."""
    
    print("\n🤖 Automation Example")
    print("=" * 30)
    
    db = setup_example()
    
    # Batch data to import
    papers_to_import = [
        {
            'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
            'arxiv': '1810.04805',
            'notes': [
                ('Bidirectional', 'Uses bidirectional training unlike GPT'),
                ('Pre-training', 'Masked LM and Next Sentence Prediction tasks')
            ],
            'entities': [
                ('transformer architecture', 'extends'),
                ('pre-training', 'introduces')
            ]
        },
        {
            'title': 'GPT-3: Language Models are Few-Shot Learners',
            'arxiv': '2005.14165',
            'notes': [
                ('Scale', '175 billion parameters, largest model at the time'),
                ('Few-shot', 'Shows emergent few-shot learning capabilities')
            ],
            'entities': [
                ('transformer architecture', 'extends'),
                ('few-shot learning', 'demonstrates')
            ]
        }
    ]
    
    print(f"Importing {len(papers_to_import)} papers...")
    
    for paper_data in papers_to_import:
        try:
            # Add source
            source_id = db.add_source(
                title=paper_data['title'],
                source_type='paper',
                identifier_type='arxiv',
                identifier_value=paper_data['arxiv']
            )
            
            # Add notes
            for note_title, note_content in paper_data['notes']:
                db.add_note(source_id, note_title, note_content)
            
            # Add entity links
            for entity_name, relation_type in paper_data['entities']:
                db.link_to_entity(source_id, entity_name, relation_type)
            
            print(f"✅ Imported: {paper_data['title'][:40]}...")
            
        except DatabaseError as e:
            print(f"❌ Failed to import {paper_data['title']}: {e}")
    
    # Show final statistics
    stats = db.get_database_stats()
    print(f"\n📊 Final Stats: {stats['total_sources']} sources, {stats['total_notes']} notes")

def example_search_and_filter():
    """Show search and filtering capabilities."""
    
    print("\n🔍 Search and Filter Example")
    print("=" * 35)
    
    db = setup_example()
    
    # Add some test data
    test_sources = [
        ("Transformer Paper 1", "paper", "arxiv", "1111.1111"),
        ("Deep Learning Book", "book", "isbn", "978-1111111111"),
        ("Transformer Tutorial", "webpage", "url", "https://example.com/1"),
        ("Neural Network Basics", "paper", "arxiv", "2222.2222"),
    ]
    
    source_ids = []
    for title, source_type, id_type, id_value in test_sources:
        try:
            source_id = db.add_source(title, source_type, id_type, id_value)
            source_ids.append(source_id)
        except DatabaseError:
            pass
    
    # Update some statuses
    if len(source_ids) >= 2:
        db.update_status(source_ids[0], "completed")
        db.update_status(source_ids[1], "reading")
    
    print("Test data created. Now demonstrating search/filter:")
    
    # Filter by type
    papers = db.list_sources(source_type="paper")
    print(f"\n📄 Papers: {len(papers)} found")
    for paper in papers:
        print(f"   • {paper['title']}")
    
    # Filter by status
    completed = db.list_sources(status="completed")
    print(f"\n✅ Completed: {len(completed)} found")
    for source in completed:
        print(f"   • {source['title']}")
    
    # Search by title (simple implementation)
    all_sources = db.list_sources(limit=100)
    transformer_sources = [s for s in all_sources if 'transformer' in s['title'].lower()]
    print(f"\n🔍 Sources with 'transformer': {len(transformer_sources)} found")
    for source in transformer_sources:
        print(f"   • {source['title']}")

def example_jupyter_notebook_style():
    """Show how to use in Jupyter notebook style."""
    
    print("\n📓 Jupyter Notebook Style Usage")
    print("=" * 40)
    
    # This is how you'd use it in a Jupyter notebook
    db = setup_example()
    
    # Cell 1: Add a source
    source_id = db.add_source("Example Paper", "paper", "arxiv", "1234.5678")
    print(f"Added source: {source_id}")
    
    # Cell 2: Add notes
    db.add_note(source_id, "Summary", "This paper discusses...")
    db.add_note(source_id, "Key Points", "Main contributions are...")
    print("Added notes")
    
    # Cell 3: Visualize (would work with matplotlib in real Jupyter)
    stats = db.get_database_stats()
    print("Database overview:")
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"{key}:")
            for k, v in value.items():
                print(f"  {k}: {v}")
        else:
            print(f"{key}: {value}")
    
    # Cell 4: Export data (for analysis)
    all_sources = db.list_sources(limit=100)
    print(f"\nExported {len(all_sources)} sources for analysis")
    
    # In a real notebook, you could do:
    # import pandas as pd
    # df = pd.DataFrame(all_sources)
    # df.plot(kind='bar', x='type')

def main():
    """Run all examples."""
    
    print("🐍 Literature Manager - Direct Python Usage")
    print("=" * 55)
    print("This shows how to use the literature manager directly in Python")
    print("without any MCP client - perfect for scripts and automation!")
    
    # Run examples
    db = example_basic_usage()
    example_automation_script()
    example_search_and_filter()
    example_jupyter_notebook_style()
    
    print("\n🎉 All examples completed!")
    print("\nFiles created:")
    print("- direct_usage_example.db (example database)")
    print("\nHow to use in your own code:")
    print("1. Import: from src.database import LiteratureDatabase")
    print("2. Create: db = LiteratureDatabase('your_database.db')")
    print("3. Use: db.add_source(), db.add_note(), etc.")
    print("\nOr use the CLI: python cli.py --help")

if __name__ == "__main__":
    main()