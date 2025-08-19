#!/usr/bin/env python3
"""
Command Line Interface for Literature Manager

Use the literature manager directly from the command line without MCP.
This provides all the functionality through simple commands.
"""

import argparse
import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.database import LiteratureDatabase, DatabaseError
from src.utils import format_source_summary
from src.models import VALID_SOURCE_TYPES, VALID_IDENTIFIER_TYPES, VALID_STATUS_VALUES, VALID_RELATION_TYPES

def get_database():
    """Get database instance from environment variable."""
    db_path = os.environ.get('LITERATURE_DB_PATH')
    if not db_path:
        print("❌ Error: LITERATURE_DB_PATH environment variable not set")
        print("Set it with: export LITERATURE_DB_PATH=/path/to/your/literature.db")
        sys.exit(1)
    
    if not Path(db_path).exists():
        print(f"❌ Error: Database not found at {db_path}")
        print("Create it with: python setup_database.py")
        sys.exit(1)
    
    return LiteratureDatabase(db_path)

def cmd_add_source(args):
    """Add a new source."""
    try:
        db = get_database()
        source_id = db.add_source(args.title, args.type, args.identifier_type, args.identifier_value)
        
        # Add initial note if provided
        if args.note_title and args.note_content:
            db.add_note(source_id, args.note_title, args.note_content)
        
        source = db.get_source_by_id(source_id)
        print("✅ Successfully added source:")
        print(format_source_summary(source))
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def cmd_add_note(args):
    """Add a note to an existing source."""
    try:
        db = get_database()
        source = db.find_source_by_identifier(args.identifier_type, args.identifier_value, args.type)
        
        if not source:
            print(f"❌ Source not found: {args.title}")
            sys.exit(1)
        
        db.add_note(source['id'], args.note_title, args.note_content)
        updated_source = db.get_source_by_id(source['id'])
        
        print(f"✅ Added note '{args.note_title}' to {args.title}")
        print(format_source_summary(updated_source))
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def cmd_update_status(args):
    """Update source status."""
    try:
        db = get_database()
        source = db.find_source_by_identifier(args.identifier_type, args.identifier_value, args.type)
        
        if not source:
            print(f"❌ Source not found: {args.title}")
            sys.exit(1)
        
        db.update_status(source['id'], args.status)
        updated_source = db.get_source_by_id(source['id'])
        
        print(f"✅ Updated status of '{args.title}' to {args.status}")
        print(format_source_summary(updated_source))
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def cmd_link_entity(args):
    """Link source to entity."""
    try:
        db = get_database()
        source = db.find_source_by_identifier(args.identifier_type, args.identifier_value, args.type)
        
        if not source:
            print(f"❌ Source not found: {args.title}")
            sys.exit(1)
        
        db.link_to_entity(source['id'], args.entity_name, args.relation_type, args.notes)
        updated_source = db.get_source_by_id(source['id'])
        
        print(f"✅ Linked '{args.title}' to entity '{args.entity_name}' with relation '{args.relation_type}'")
        print(format_source_summary(updated_source))
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def cmd_show_source(args):
    """Show detailed source information."""
    try:
        db = get_database()
        source = db.find_source_by_identifier(args.identifier_type, args.identifier_value, args.type)
        
        if not source:
            print(f"❌ Source not found: {args.title}")
            sys.exit(1)
        
        full_source = db.get_source_by_id(source['id'])
        print("📚 Source Details:")
        print("=" * 50)
        print(format_source_summary(full_source))
        
        # Show detailed notes
        if full_source['notes']:
            print("\n📝 Notes:")
            for note in full_source['notes']:
                print(f"\n  📌 {note['title']}")
                print(f"     {note['content']}")
                print(f"     Created: {note['created_at']}")
        
        # Show entity links
        if full_source['entity_links']:
            print("\n🔗 Entity Links:")
            for link in full_source['entity_links']:
                print(f"  • {link['entity_name']} ({link['relation_type']})")
                if link['notes']:
                    print(f"    Notes: {link['notes']}")
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def cmd_list_sources(args):
    """List sources with optional filtering."""
    try:
        db = get_database()
        sources = db.list_sources(args.type, args.status, args.limit)
        
        if not sources:
            print("📚 No sources found")
            return
        
        filter_desc = []
        if args.type:
            filter_desc.append(f"type={args.type}")
        if args.status:
            filter_desc.append(f"status={args.status}")
        
        filter_text = f" (filtered by {', '.join(filter_desc)})" if filter_desc else ""
        print(f"📚 Found {len(sources)} sources{filter_text}:")
        print("=" * 50)
        
        for i, source in enumerate(sources, 1):
            print(f"{i}. {source['title']}")
            print(f"   Type: {source['type'].title()}, Status: {source['status'].title()}")
            print(f"   Created: {source['created_at']}")
            print()
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def cmd_search_sources(args):
    """Search sources by title."""
    try:
        db = get_database()
        all_sources = db.list_sources(limit=1000)
        
        # Simple search by title
        query_lower = args.query.lower()
        matches = []
        
        for source in all_sources:
            if query_lower in source['title'].lower():
                matches.append(source)
        
        if not matches:
            print(f"🔍 No sources found matching '{args.query}'")
            return
        
        print(f"🔍 Found {len(matches)} sources matching '{args.query}':")
        print("=" * 50)
        
        for i, source in enumerate(matches[:args.limit], 1):
            print(f"{i}. {source['title']}")
            print(f"   Type: {source['type'].title()}, Status: {source['status'].title()}")
            print()
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def cmd_stats(args):
    """Show database statistics."""
    try:
        db = get_database()
        stats = db.get_database_stats()
        
        print("📊 Database Statistics")
        print("=" * 30)
        print(f"Total Sources: {stats['total_sources']}")
        print(f"Total Notes: {stats['total_notes']}")
        print(f"Total Entity Links: {stats['total_entity_links']}")
        
        if stats['sources_by_type']:
            print("\nSources by Type:")
            for source_type, count in stats['sources_by_type'].items():
                print(f"  {source_type.title()}: {count}")
        
        if stats['sources_by_status']:
            print("\nSources by Status:")
            for status, count in stats['sources_by_status'].items():
                print(f"  {status.title()}: {count}")
        
    except DatabaseError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def cmd_help(args):
    """Show help information."""
    help_text = """
📚 Literature Manager CLI Help

BASIC COMMANDS:
  add-source     Add a new source (paper, book, webpage, etc.)
  add-note       Add a note to an existing source
  update-status  Change reading status
  link-entity    Connect source to a concept/entity
  show           Show detailed source information
  list           List sources with optional filtering
  search         Search sources by title
  stats          Show database statistics

EXAMPLES:
  # Add a research paper
  python cli.py add-source "Attention Is All You Need" paper arxiv 1706.03762

  # Add a note
  python cli.py add-note "Attention Is All You Need" paper arxiv 1706.03762 \\
    --note-title "Key Insight" --note-content "Transformers eliminate recurrence"

  # Update status
  python cli.py update-status "Attention Is All You Need" paper arxiv 1706.03762 completed

  # Link to entity
  python cli.py link-entity "Attention Is All You Need" paper arxiv 1706.03762 \\
    "transformer architecture" introduces

  # Show source details
  python cli.py show "Attention Is All You Need" paper arxiv 1706.03762

  # List sources
  python cli.py list --type paper --status unread --limit 10

  # Search sources
  python cli.py search "transformer" --limit 5

  # Show statistics
  python cli.py stats

VALID VALUES:
  Source Types: paper, webpage, book, video, blog
  Identifier Types: arxiv, doi, isbn, url, semantic_scholar
  Status Values: unread, reading, completed, archived
  Relation Types: discusses, introduces, extends, evaluates, applies, critiques

SETUP:
  1. Create database: python setup_database.py
  2. Set environment: export LITERATURE_DB_PATH=/path/to/literature.db
  3. Use commands above

For more help, see: https://github.com/Amruth22/literature-manager-mcp
"""
    print(help_text)

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Literature Manager - Direct Python CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add source command
    add_parser = subparsers.add_parser('add-source', help='Add a new source')
    add_parser.add_argument('title', help='Source title')
    add_parser.add_argument('type', choices=VALID_SOURCE_TYPES, help='Source type')
    add_parser.add_argument('identifier_type', choices=VALID_IDENTIFIER_TYPES, help='Identifier type')
    add_parser.add_argument('identifier_value', help='Identifier value')
    add_parser.add_argument('--note-title', help='Initial note title')
    add_parser.add_argument('--note-content', help='Initial note content')
    add_parser.set_defaults(func=cmd_add_source)
    
    # Add note command
    note_parser = subparsers.add_parser('add-note', help='Add a note to source')
    note_parser.add_argument('title', help='Source title')
    note_parser.add_argument('type', choices=VALID_SOURCE_TYPES, help='Source type')
    note_parser.add_argument('identifier_type', choices=VALID_IDENTIFIER_TYPES, help='Identifier type')
    note_parser.add_argument('identifier_value', help='Identifier value')
    note_parser.add_argument('note_title', help='Note title')
    note_parser.add_argument('note_content', help='Note content')
    note_parser.set_defaults(func=cmd_add_note)
    
    # Update status command
    status_parser = subparsers.add_parser('update-status', help='Update source status')
    status_parser.add_argument('title', help='Source title')
    status_parser.add_argument('type', choices=VALID_SOURCE_TYPES, help='Source type')
    status_parser.add_argument('identifier_type', choices=VALID_IDENTIFIER_TYPES, help='Identifier type')
    status_parser.add_argument('identifier_value', help='Identifier value')
    status_parser.add_argument('status', choices=VALID_STATUS_VALUES, help='New status')
    status_parser.set_defaults(func=cmd_update_status)
    
    # Link entity command
    link_parser = subparsers.add_parser('link-entity', help='Link source to entity')
    link_parser.add_argument('title', help='Source title')
    link_parser.add_argument('type', choices=VALID_SOURCE_TYPES, help='Source type')
    link_parser.add_argument('identifier_type', choices=VALID_IDENTIFIER_TYPES, help='Identifier type')
    link_parser.add_argument('identifier_value', help='Identifier value')
    link_parser.add_argument('entity_name', help='Entity name')
    link_parser.add_argument('relation_type', choices=VALID_RELATION_TYPES, help='Relation type')
    link_parser.add_argument('--notes', help='Optional notes about the relationship')
    link_parser.set_defaults(func=cmd_link_entity)
    
    # Show source command
    show_parser = subparsers.add_parser('show', help='Show source details')
    show_parser.add_argument('title', help='Source title')
    show_parser.add_argument('type', choices=VALID_SOURCE_TYPES, help='Source type')
    show_parser.add_argument('identifier_type', choices=VALID_IDENTIFIER_TYPES, help='Identifier type')
    show_parser.add_argument('identifier_value', help='Identifier value')
    show_parser.set_defaults(func=cmd_show_source)
    
    # List sources command
    list_parser = subparsers.add_parser('list', help='List sources')
    list_parser.add_argument('--type', choices=VALID_SOURCE_TYPES, help='Filter by source type')
    list_parser.add_argument('--status', choices=VALID_STATUS_VALUES, help='Filter by status')
    list_parser.add_argument('--limit', type=int, default=20, help='Maximum number of results')
    list_parser.set_defaults(func=cmd_list_sources)
    
    # Search sources command
    search_parser = subparsers.add_parser('search', help='Search sources by title')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--limit', type=int, default=10, help='Maximum number of results')
    search_parser.set_defaults(func=cmd_search_sources)
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show database statistics')
    stats_parser.set_defaults(func=cmd_stats)
    
    # Help command
    help_parser = subparsers.add_parser('help', help='Show detailed help')
    help_parser.set_defaults(func=cmd_help)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Execute command
    args.func(args)

if __name__ == "__main__":
    main()