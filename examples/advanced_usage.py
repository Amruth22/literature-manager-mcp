#!/usr/bin/env python3
"""
Advanced Usage Examples for Literature Manager

This file demonstrates more complex workflows and batch operations.
"""

import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.database import LiteratureDatabase, DatabaseError
from src.utils import create_example_data, format_source_summary

def setup_advanced_database():
    """Create a database with more complex example data."""
    
    db_path = "advanced_literature.db"
    
    # Remove existing database
    if Path(db_path).exists():
        Path(db_path).unlink()
    
    # Create database (simplified setup)
    import sqlite3
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        
        # Create tables
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

def example_1_batch_import():
    """Example 1: Batch import of multiple sources."""
    
    print("📚 Example 1: Batch Import")
    print("=" * 40)
    
    db_path = setup_advanced_database()
    db = LiteratureDatabase(db_path)
    
    # Define a collection of sources to import
    sources_to_import = [
        {
            'title': 'Attention Is All You Need',
            'type': 'paper',
            'identifier_type': 'arxiv',
            'identifier_value': '1706.03762',
            'notes': [
                ('Key Innovation', 'Introduces transformer architecture'),
                ('Impact', 'Revolutionized NLP and became foundation for GPT, BERT, etc.')
            ],
            'entities': [
                ('transformer architecture', 'introduces', 'First paper to introduce transformers'),
                ('attention mechanism', 'discusses', 'Detailed explanation of self-attention')
            ]
        },
        {
            'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
            'type': 'paper',
            'identifier_type': 'arxiv',
            'identifier_value': '1810.04805',
            'notes': [
                ('Bidirectional Context', 'Uses bidirectional training unlike GPT'),
                ('Pre-training Tasks', 'Masked LM and Next Sentence Prediction')
            ],
            'entities': [
                ('transformer architecture', 'extends', 'Builds on transformer for bidirectional understanding'),
                ('pre-training', 'introduces', 'Popularized pre-training approach in NLP')
            ]
        },
        {
            'title': 'Deep Learning',
            'type': 'book',
            'identifier_type': 'isbn',
            'identifier_value': '978-0262035613',
            'notes': [
                ('Comprehensive Coverage', 'Covers fundamentals to advanced topics'),
                ('Mathematical Rigor', 'Strong mathematical foundation')
            ],
            'entities': [
                ('deep learning', 'discusses', 'Comprehensive textbook on deep learning'),
                ('neural networks', 'discusses', 'Detailed coverage of neural network architectures')
            ]
        }
    ]
    
    imported_ids = []
    
    try:
        for source_data in sources_to_import:
            print(f"\nImporting: {source_data['title']}")
            
            # Add the source
            source_id = db.add_source(
                title=source_data['title'],
                source_type=source_data['type'],
                identifier_type=source_data['identifier_type'],
                identifier_value=source_data['identifier_value']
            )
            imported_ids.append(source_id)
            print(f"  ✅ Added source: {source_id}")
            
            # Add notes
            for note_title, note_content in source_data.get('notes', []):
                db.add_note(source_id, note_title, note_content)
                print(f"  📝 Added note: {note_title}")
            
            # Add entity links
            for entity_name, relation_type, notes in source_data.get('entities', []):
                db.link_to_entity(source_id, entity_name, relation_type, notes)
                print(f"  🔗 Linked to entity: {entity_name} ({relation_type})")
        
        print(f"\n🎉 Successfully imported {len(imported_ids)} sources!")
        return db, imported_ids
        
    except DatabaseError as e:
        print(f"❌ Import failed: {e}")
        return None, []

def example_2_research_workflow(db, source_ids):
    """Example 2: Simulate a research workflow."""
    
    print("\n🔬 Example 2: Research Workflow")
    print("=" * 40)
    
    if not db or not source_ids:
        print("❌ No sources available from previous example")
        return
    
    try:
        # Step 1: Mark papers as "reading" when starting research
        print("Step 1: Starting to read papers...")
        for source_id in source_ids[:2]:  # First two papers
            db.update_status(source_id, "reading")
            source = db.get_source_by_id(source_id)
            print(f"  📖 Now reading: {source['title']}")
        
        # Step 2: Add detailed notes as you read
        print("\nStep 2: Adding detailed reading notes...")
        
        # Add detailed notes to Attention paper
        attention_id = source_ids[0]
        detailed_notes = [
            ("Architecture Details", "Encoder-decoder structure with 6 layers each. Multi-head attention with 8 heads."),
            ("Training Details", "Trained on WMT 2014 En-De dataset. Used Adam optimizer with custom learning rate schedule."),
            ("Results", "Achieved SOTA on WMT 2014 En-De (28.4 BLEU) and En-Fr (41.8 BLEU) translation tasks."),
            ("Limitations", "Quadratic complexity with sequence length. Memory intensive for long sequences.")
        ]
        
        for note_title, note_content in detailed_notes:
            db.add_note(attention_id, note_title, note_content)
            print(f"  📝 Added detailed note: {note_title}")
        
        # Step 3: Connect related concepts
        print("\nStep 3: Building knowledge connections...")
        
        # Add more entity connections
        bert_id = source_ids[1]
        additional_connections = [
            (bert_id, "masked language modeling", "introduces", "Key pre-training task in BERT"),
            (bert_id, "fine-tuning", "discusses", "Shows how to fine-tune BERT for downstream tasks"),
            (attention_id, "positional encoding", "discusses", "Uses sinusoidal positional encodings"),
            (attention_id, "multi-head attention", "introduces", "Key innovation allowing parallel attention")
        ]
        
        for source_id, entity, relation, notes in additional_connections:
            db.link_to_entity(source_id, entity, relation, notes)
            source = db.get_source_by_id(source_id)
            print(f"  🔗 Connected '{source['title'][:30]}...' to '{entity}'")
        
        # Step 4: Mark completed papers
        print("\nStep 4: Completing papers...")
        for source_id in source_ids[:2]:
            db.update_status(source_id, "completed")
            source = db.get_source_by_id(source_id)
            print(f"  ✅ Completed: {source['title']}")
        
        print("\n🎯 Research workflow completed!")
        
    except DatabaseError as e:
        print(f"❌ Workflow failed: {e}")

def example_3_knowledge_exploration(db):
    """Example 3: Explore knowledge connections."""
    
    print("\n🧠 Example 3: Knowledge Exploration")
    print("=" * 40)
    
    if not db:
        print("❌ No database available")
        return
    
    try:
        # Get all sources and analyze connections
        all_sources = db.list_sources(limit=100)
        
        print(f"Total sources in database: {len(all_sources)}")
        
        # Analyze by type
        type_counts = {}
        status_counts = {}
        
        for source in all_sources:
            source_type = source['type']
            status = source['status']
            
            type_counts[source_type] = type_counts.get(source_type, 0) + 1
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print("\nSources by type:")
        for source_type, count in type_counts.items():
            print(f"  {source_type.title()}: {count}")
        
        print("\nSources by status:")
        for status, count in status_counts.items():
            print(f"  {status.title()}: {count}")
        
        # Find sources with most notes
        print("\nSources with most notes:")
        sources_with_notes = []
        
        for source in all_sources:
            full_source = db.get_source_by_id(source['id'])
            note_count = len(full_source['notes'])
            if note_count > 0:
                sources_with_notes.append((full_source, note_count))
        
        # Sort by note count
        sources_with_notes.sort(key=lambda x: x[1], reverse=True)
        
        for source, note_count in sources_with_notes[:3]:  # Top 3
            print(f"  📚 {source['title'][:40]}... ({note_count} notes)")
        
        # Find most connected entities
        print("\nMost connected entities:")
        entity_connections = {}
        
        for source in all_sources:
            full_source = db.get_source_by_id(source['id'])
            for link in full_source['entity_links']:
                entity = link['entity_name']
                entity_connections[entity] = entity_connections.get(entity, 0) + 1
        
        # Sort by connection count
        sorted_entities = sorted(entity_connections.items(), key=lambda x: x[1], reverse=True)
        
        for entity, count in sorted_entities[:5]:  # Top 5
            print(f"  🔗 {entity}: {count} connections")
        
        # Show detailed view of most connected entity
        if sorted_entities:
            top_entity = sorted_entities[0][0]
            print(f"\nDetailed view of '{top_entity}':")
            
            for source in all_sources:
                full_source = db.get_source_by_id(source['id'])
                for link in full_source['entity_links']:
                    if link['entity_name'] == top_entity:
                        print(f"  📄 {full_source['title'][:40]}... ({link['relation_type']})")
        
    except DatabaseError as e:
        print(f"❌ Exploration failed: {e}")

def example_4_export_summary(db):
    """Example 4: Export a research summary."""
    
    print("\n📊 Example 4: Research Summary Export")
    print("=" * 40)
    
    if not db:
        print("❌ No database available")
        return
    
    try:
        # Generate a comprehensive summary
        stats = db.get_database_stats()
        all_sources = db.list_sources(limit=100)
        
        summary_lines = []
        summary_lines.append("# Literature Review Summary")
        summary_lines.append(f"Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        summary_lines.append("")
        
        # Overview statistics
        summary_lines.append("## Overview")
        summary_lines.append(f"- Total Sources: {stats['total_sources']}")
        summary_lines.append(f"- Total Notes: {stats['total_notes']}")
        summary_lines.append(f"- Total Entity Links: {stats['total_entity_links']}")
        summary_lines.append("")
        
        # Sources by type
        if stats['sources_by_type']:
            summary_lines.append("## Sources by Type")
            for source_type, count in stats['sources_by_type'].items():
                summary_lines.append(f"- {source_type.title()}: {count}")
            summary_lines.append("")
        
        # Reading progress
        if stats['sources_by_status']:
            summary_lines.append("## Reading Progress")
            for status, count in stats['sources_by_status'].items():
                summary_lines.append(f"- {status.title()}: {count}")
            summary_lines.append("")
        
        # Detailed source list
        summary_lines.append("## Detailed Source List")
        
        for source in all_sources:
            full_source = db.get_source_by_id(source['id'])
            summary_lines.append(f"### {full_source['title']}")
            summary_lines.append(f"- **Type**: {full_source['type'].title()}")
            summary_lines.append(f"- **Status**: {full_source['status'].title()}")
            
            # Identifiers
            if full_source['identifiers']:
                id_parts = []
                for id_type, id_value in full_source['identifiers'].items():
                    id_parts.append(f"{id_type}: {id_value}")
                summary_lines.append(f"- **Identifiers**: {', '.join(id_parts)}")
            
            # Notes
            if full_source['notes']:
                summary_lines.append(f"- **Notes** ({len(full_source['notes'])}):")
                for note in full_source['notes']:
                    summary_lines.append(f"  - **{note['title']}**: {note['content'][:100]}...")
            
            # Entity links
            if full_source['entity_links']:
                summary_lines.append(f"- **Connected Concepts** ({len(full_source['entity_links'])}):")
                for link in full_source['entity_links']:
                    summary_lines.append(f"  - {link['entity_name']} ({link['relation_type']})")
            
            summary_lines.append("")
        
        # Write summary to file
        summary_content = '\n'.join(summary_lines)
        summary_file = "literature_summary.md"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        print(f"📄 Summary exported to: {summary_file}")
        print(f"📊 Summary contains {len(summary_lines)} lines")
        
        # Show preview
        print("\nPreview (first 10 lines):")
        for line in summary_lines[:10]:
            print(f"  {line}")
        
        if len(summary_lines) > 10:
            print("  ...")
        
    except Exception as e:
        print(f"❌ Export failed: {e}")

def main():
    """Run all advanced examples."""
    
    print("🚀 Literature Manager - Advanced Usage Examples")
    print("=" * 55)
    
    # Run examples in sequence
    db, source_ids = example_1_batch_import()
    
    if db and source_ids:
        example_2_research_workflow(db, source_ids)
        example_3_knowledge_exploration(db)
        example_4_export_summary(db)
    
    print("\n🎉 Advanced examples completed!")
    print("\nFiles created:")
    print("- advanced_literature.db (example database)")
    print("- literature_summary.md (exported summary)")
    print("\nThese examples show how to:")
    print("1. Import multiple sources efficiently")
    print("2. Manage a complete research workflow")
    print("3. Explore knowledge connections")
    print("4. Export summaries for sharing")

if __name__ == "__main__":
    main()