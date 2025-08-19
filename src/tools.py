"""
MCP Tools for Literature Manager

This module defines all the tools available through the MCP interface.
Each tool is designed to be beginner-friendly with clear documentation.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastmcp import FastMCP

from .database import LiteratureDatabase, DatabaseError
from .models import VALID_SOURCE_TYPES, VALID_IDENTIFIER_TYPES, VALID_STATUS_VALUES, VALID_RELATION_TYPES
from .utils import format_source_summary, validate_input_data, search_sources_by_title

# Initialize FastMCP server
mcp = FastMCP("Literature Manager")

# Get database path from environment
DB_PATH = os.environ.get('LITERATURE_DB_PATH')
if not DB_PATH:
    raise ValueError("LITERATURE_DB_PATH environment variable must be set")

def get_database() -> LiteratureDatabase:
    """Get database instance."""
    return LiteratureDatabase(DB_PATH)

@mcp.tool()
def add_source(
    title: str,
    source_type: str,
    identifier_type: str,
    identifier_value: str,
    initial_note_title: Optional[str] = None,
    initial_note_content: Optional[str] = None
) -> Dict[str, Any]:
    """
    Add a new source to your literature collection.
    
    Args:
        title: Title of the source (e.g., "Attention Is All You Need")
        source_type: Type of source - must be one of: paper, webpage, book, video, blog
        identifier_type: Type of identifier - must be one of: arxiv, doi, isbn, url, semantic_scholar
        identifier_value: Value of the identifier (e.g., "1706.03762" for arXiv)
        initial_note_title: Optional title for an initial note
        initial_note_content: Optional content for an initial note
    
    Returns:
        Dictionary with operation result and source details
    
    Examples:
        # Add a research paper
        add_source("Attention Is All You Need", "paper", "arxiv", "1706.03762")
        
        # Add a book with initial note
        add_source("Deep Learning", "book", "isbn", "978-0262035613", 
                  "First Impression", "Comprehensive deep learning textbook")
    """
    try:
        # Validate input
        data = {
            'title': title,
            'source_type': source_type,
            'identifier_type': identifier_type,
            'identifier_value': identifier_value
        }
        errors = validate_input_data(data)
        if errors:
            return {
                'success': False,
                'error': 'Validation failed',
                'details': errors
            }
        
        db = get_database()
        
        # Add the source
        source_id = db.add_source(title, source_type, identifier_type, identifier_value)
        
        # Add initial note if provided
        if initial_note_title and initial_note_content:
            db.add_note(source_id, initial_note_title, initial_note_content)
        
        # Get complete source details
        source = db.get_source_by_id(source_id)
        
        return {
            'success': True,
            'message': f'Successfully added {source_type}: {title}',
            'source': source,
            'summary': format_source_summary(source)
        }
        
    except DatabaseError as e:
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

@mcp.tool()
def add_note(
    title: str,
    source_type: str,
    identifier_type: str,
    identifier_value: str,
    note_title: str,
    note_content: str
) -> Dict[str, Any]:
    """
    Add a note to an existing source.
    
    Args:
        title: Title of the source
        source_type: Type of source
        identifier_type: Type of identifier
        identifier_value: Value of the identifier
        note_title: Title for the new note
        note_content: Content of the note
    
    Returns:
        Dictionary with operation result
    
    Examples:
        add_note("Attention Is All You Need", "paper", "arxiv", "1706.03762",
                "Key Insights", "The transformer eliminates recurrence...")
    """
    try:
        db = get_database()
        
        # Find the source
        source = db.find_source_by_identifier(identifier_type, identifier_value, source_type)
        if not source:
            return {
                'success': False,
                'error': f'Source not found: {title}'
            }
        
        # Add the note
        db.add_note(source['id'], note_title, note_content)
        
        # Get updated source details
        updated_source = db.get_source_by_id(source['id'])
        
        return {
            'success': True,
            'message': f'Added note "{note_title}" to {title}',
            'source': updated_source,
            'summary': format_source_summary(updated_source)
        }
        
    except DatabaseError as e:
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

@mcp.tool()
def update_status(
    title: str,
    source_type: str,
    identifier_type: str,
    identifier_value: str,
    new_status: str
) -> Dict[str, Any]:
    """
    Update the reading status of a source.
    
    Args:
        title: Title of the source
        source_type: Type of source
        identifier_type: Type of identifier
        identifier_value: Value of the identifier
        new_status: New status - must be one of: unread, reading, completed, archived
    
    Returns:
        Dictionary with operation result
    
    Examples:
        update_status("Attention Is All You Need", "paper", "arxiv", "1706.03762", "completed")
    """
    try:
        if new_status not in VALID_STATUS_VALUES:
            return {
                'success': False,
                'error': f'Invalid status. Must be one of: {", ".join(VALID_STATUS_VALUES)}'
            }
        
        db = get_database()
        
        # Find the source
        source = db.find_source_by_identifier(identifier_type, identifier_value, source_type)
        if not source:
            return {
                'success': False,
                'error': f'Source not found: {title}'
            }
        
        # Update status
        db.update_status(source['id'], new_status)
        
        # Get updated source details
        updated_source = db.get_source_by_id(source['id'])
        
        return {
            'success': True,
            'message': f'Updated status of "{title}" to {new_status}',
            'source': updated_source,
            'summary': format_source_summary(updated_source)
        }
        
    except DatabaseError as e:
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

@mcp.tool()
def link_to_entity(
    title: str,
    source_type: str,
    identifier_type: str,
    identifier_value: str,
    entity_name: str,
    relation_type: str,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Link a source to an entity in your knowledge graph.
    
    Args:
        title: Title of the source
        source_type: Type of source
        identifier_type: Type of identifier
        identifier_value: Value of the identifier
        entity_name: Name of the entity to link to
        relation_type: Type of relationship - must be one of: discusses, introduces, extends, evaluates, applies, critiques
        notes: Optional notes about the relationship
    
    Returns:
        Dictionary with operation result
    
    Examples:
        link_to_entity("Attention Is All You Need", "paper", "arxiv", "1706.03762",
                      "transformer architecture", "introduces", 
                      "First paper to introduce the transformer model")
    """
    try:
        if relation_type not in VALID_RELATION_TYPES:
            return {
                'success': False,
                'error': f'Invalid relation type. Must be one of: {", ".join(VALID_RELATION_TYPES)}'
            }
        
        db = get_database()
        
        # Find the source
        source = db.find_source_by_identifier(identifier_type, identifier_value, source_type)
        if not source:
            return {
                'success': False,
                'error': f'Source not found: {title}'
            }
        
        # Create the link
        db.link_to_entity(source['id'], entity_name, relation_type, notes)
        
        # Get updated source details
        updated_source = db.get_source_by_id(source['id'])
        
        return {
            'success': True,
            'message': f'Linked "{title}" to entity "{entity_name}" with relation "{relation_type}"',
            'source': updated_source,
            'summary': format_source_summary(updated_source)
        }
        
    except DatabaseError as e:
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

@mcp.tool()
def get_source_details(
    title: str,
    source_type: str,
    identifier_type: str,
    identifier_value: str
) -> Dict[str, Any]:
    """
    Get complete details about a source including notes and entity links.
    
    Args:
        title: Title of the source
        source_type: Type of source
        identifier_type: Type of identifier
        identifier_value: Value of the identifier
    
    Returns:
        Dictionary with source details
    
    Examples:
        get_source_details("Attention Is All You Need", "paper", "arxiv", "1706.03762")
    """
    try:
        db = get_database()
        
        # Find the source
        source = db.find_source_by_identifier(identifier_type, identifier_value, source_type)
        if not source:
            return {
                'success': False,
                'error': f'Source not found: {title}'
            }
        
        # Get complete details
        complete_source = db.get_source_by_id(source['id'])
        
        return {
            'success': True,
            'source': complete_source,
            'summary': format_source_summary(complete_source)
        }
        
    except DatabaseError as e:
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

@mcp.tool()
def list_sources(
    source_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20
) -> Dict[str, Any]:
    """
    List sources with optional filtering.
    
    Args:
        source_type: Optional filter by source type (paper, book, etc.)
        status: Optional filter by status (unread, reading, etc.)
        limit: Maximum number of sources to return (default: 20)
    
    Returns:
        Dictionary with list of sources
    
    Examples:
        list_sources()  # List all sources
        list_sources(source_type="paper")  # List only papers
        list_sources(status="unread", limit=10)  # List 10 unread sources
    """
    try:
        db = get_database()
        
        # Validate filters
        if source_type and source_type not in VALID_SOURCE_TYPES:
            return {
                'success': False,
                'error': f'Invalid source type. Must be one of: {", ".join(VALID_SOURCE_TYPES)}'
            }
        
        if status and status not in VALID_STATUS_VALUES:
            return {
                'success': False,
                'error': f'Invalid status. Must be one of: {", ".join(VALID_STATUS_VALUES)}'
            }
        
        # Get sources
        sources = db.list_sources(source_type, status, limit)
        
        # Create summary
        filter_desc = []
        if source_type:
            filter_desc.append(f"type={source_type}")
        if status:
            filter_desc.append(f"status={status}")
        
        filter_text = f" (filtered by {', '.join(filter_desc)})" if filter_desc else ""
        
        return {
            'success': True,
            'message': f'Found {len(sources)} sources{filter_text}',
            'sources': sources,
            'count': len(sources)
        }
        
    except DatabaseError as e:
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

@mcp.tool()
def search_sources(query: str, limit: int = 10) -> Dict[str, Any]:
    """
    Search sources by title.
    
    Args:
        query: Search query (searches in titles)
        limit: Maximum number of results (default: 10)
    
    Returns:
        Dictionary with search results
    
    Examples:
        search_sources("transformer")
        search_sources("deep learning", limit=5)
    """
    try:
        db = get_database()
        
        # Get all sources and search
        all_sources = db.list_sources(limit=1000)  # Get more for searching
        matches = search_sources_by_title(all_sources, query)
        
        # Limit results
        limited_matches = matches[:limit]
        
        return {
            'success': True,
            'message': f'Found {len(limited_matches)} sources matching "{query}"',
            'sources': limited_matches,
            'query': query,
            'count': len(limited_matches)
        }
        
    except DatabaseError as e:
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

@mcp.tool()
def database_stats() -> Dict[str, Any]:
    """
    Get statistics about your literature database.
    
    Returns:
        Dictionary with database statistics
    
    Examples:
        database_stats()
    """
    try:
        db = get_database()
        stats = db.get_database_stats()
        
        # Format the stats nicely
        summary_lines = []
        summary_lines.append(f"📊 Database Statistics")
        summary_lines.append(f"Total Sources: {stats['total_sources']}")
        summary_lines.append(f"Total Notes: {stats['total_notes']}")
        summary_lines.append(f"Total Entity Links: {stats['total_entity_links']}")
        
        if stats['sources_by_type']:
            summary_lines.append("\nSources by Type:")
            for source_type, count in stats['sources_by_type'].items():
                summary_lines.append(f"  {source_type.title()}: {count}")
        
        if stats['sources_by_status']:
            summary_lines.append("\nSources by Status:")
            for status, count in stats['sources_by_status'].items():
                summary_lines.append(f"  {status.title()}: {count}")
        
        return {
            'success': True,
            'stats': stats,
            'summary': '\n'.join(summary_lines)
        }
        
    except DatabaseError as e:
        return {
            'success': False,
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'Unexpected error: {str(e)}'
        }

@mcp.tool()
def get_help() -> Dict[str, Any]:
    """
    Get help information about available commands and usage.
    
    Returns:
        Dictionary with help information
    """
    help_text = """
📚 Literature Manager Help

BASIC COMMANDS:
• add_source() - Add a new paper, book, or other source
• add_note() - Add notes to existing sources
• update_status() - Change reading status (unread/reading/completed/archived)
• get_source_details() - Get complete information about a source

SEARCH & LIST:
• list_sources() - List all sources with optional filtering
• search_sources() - Search sources by title
• database_stats() - Show database statistics

KNOWLEDGE GRAPH:
• link_to_entity() - Connect sources to concepts/entities

VALID VALUES:
• Source Types: paper, webpage, book, video, blog
• Identifier Types: arxiv, doi, isbn, url, semantic_scholar
• Status Values: unread, reading, completed, archived
• Relation Types: discusses, introduces, extends, evaluates, applies, critiques

EXAMPLES:
1. Add a paper:
   add_source("Attention Is All You Need", "paper", "arxiv", "1706.03762")

2. Add a note:
   add_note("Attention Is All You Need", "paper", "arxiv", "1706.03762", 
           "Key Insight", "Transformers eliminate recurrence...")

3. Update status:
   update_status("Attention Is All You Need", "paper", "arxiv", "1706.03762", "completed")

4. Link to concept:
   link_to_entity("Attention Is All You Need", "paper", "arxiv", "1706.03762",
                 "transformer architecture", "introduces")

For more examples, see the documentation at:
https://github.com/Amruth22/literature-manager-mcp
"""
    
    return {
        'success': True,
        'help': help_text
    }