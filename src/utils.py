"""
Utility Functions for Literature Manager

This module contains helper functions used throughout the application.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from .models import VALID_SOURCE_TYPES, VALID_IDENTIFIER_TYPES

def clean_title(title: str) -> str:
    """
    Clean and normalize a title string.
    
    Args:
        title: Raw title string
        
    Returns:
        str: Cleaned title
    """
    # Remove extra whitespace
    title = re.sub(r'\s+', ' ', title.strip())
    
    # Remove common prefixes/suffixes
    title = re.sub(r'^(A|An|The)\s+', '', title, flags=re.IGNORECASE)
    
    return title

def extract_arxiv_id(text: str) -> Optional[str]:
    """
    Extract arXiv ID from various text formats.
    
    Args:
        text: Text that might contain an arXiv ID
        
    Returns:
        str: arXiv ID if found, None otherwise
    """
    # Pattern for arXiv IDs (both old and new formats)
    patterns = [
        r'(?:arxiv:)?(\d{4}\.\d{4,5}(?:v\d+)?)',  # New format: 1234.5678v1
        r'(?:arxiv:)?([a-z-]+(?:\.[A-Z]{2})?/\d{7}(?:v\d+)?)'  # Old format: math.CO/0123456v1
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def extract_doi(text: str) -> Optional[str]:
    """
    Extract DOI from text.
    
    Args:
        text: Text that might contain a DOI
        
    Returns:
        str: DOI if found, None otherwise
    """
    # DOI pattern
    pattern = r'(?:doi:)?(10\.\d+/[^\s]+)'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return None

def extract_isbn(text: str) -> Optional[str]:
    """
    Extract ISBN from text.
    
    Args:
        text: Text that might contain an ISBN
        
    Returns:
        str: ISBN if found, None otherwise
    """
    # Remove all non-digit characters except X
    cleaned = re.sub(r'[^\dX]', '', text.upper())
    
    # Check for ISBN-13 (13 digits)
    if len(cleaned) == 13 and cleaned.startswith(('978', '979')):
        return cleaned
    
    # Check for ISBN-10 (10 digits, last can be X)
    if len(cleaned) == 10:
        return cleaned
    
    return None

def validate_url(url: str) -> bool:
    """
    Validate if a string is a valid URL.
    
    Args:
        url: URL string to validate
        
    Returns:
        bool: True if valid URL
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None

def guess_source_type(title: str, identifier_type: str, identifier_value: str) -> str:
    """
    Guess the source type based on available information.
    
    Args:
        title: Title of the source
        identifier_type: Type of identifier
        identifier_value: Value of the identifier
        
    Returns:
        str: Guessed source type
    """
    # Map identifier types to likely source types
    identifier_mapping = {
        'arxiv': 'paper',
        'doi': 'paper',
        'semantic_scholar': 'paper',
        'isbn': 'book',
        'url': 'webpage'
    }
    
    if identifier_type in identifier_mapping:
        return identifier_mapping[identifier_type]
    
    # Guess from title keywords
    title_lower = title.lower()
    
    if any(word in title_lower for word in ['paper', 'article', 'journal', 'conference']):
        return 'paper'
    elif any(word in title_lower for word in ['book', 'textbook', 'handbook']):
        return 'book'
    elif any(word in title_lower for word in ['video', 'lecture', 'tutorial']):
        return 'video'
    elif any(word in title_lower for word in ['blog', 'post']):
        return 'blog'
    
    # Default to webpage
    return 'webpage'

def format_source_summary(source: Dict[str, Any]) -> str:
    """
    Format a source dictionary into a readable summary.
    
    Args:
        source: Source dictionary
        
    Returns:
        str: Formatted summary
    """
    lines = []
    lines.append(f"📚 {source['title']}")
    lines.append(f"   Type: {source['type'].title()}")
    lines.append(f"   Status: {source['status'].title()}")
    
    # Show identifiers
    if source.get('identifiers'):
        id_parts = []
        for id_type, id_value in source['identifiers'].items():
            id_parts.append(f"{id_type}: {id_value}")
        lines.append(f"   IDs: {', '.join(id_parts)}")
    
    # Show note count
    note_count = len(source.get('notes', []))
    if note_count > 0:
        lines.append(f"   Notes: {note_count}")
    
    # Show entity links
    link_count = len(source.get('entity_links', []))
    if link_count > 0:
        lines.append(f"   Entity Links: {link_count}")
    
    return '\n'.join(lines)

def search_sources_by_title(sources: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
    """
    Search sources by title using fuzzy matching.
    
    Args:
        sources: List of source dictionaries
        query: Search query
        
    Returns:
        List of matching sources, sorted by relevance
    """
    query_lower = query.lower()
    matches = []
    
    for source in sources:
        title_lower = source['title'].lower()
        
        # Exact match gets highest score
        if query_lower == title_lower:
            matches.append((source, 100))
        # Contains query gets medium score
        elif query_lower in title_lower:
            matches.append((source, 50))
        # Word match gets lower score
        elif any(word in title_lower for word in query_lower.split()):
            matches.append((source, 25))
    
    # Sort by score (descending) and return sources
    matches.sort(key=lambda x: x[1], reverse=True)
    return [match[0] for match in matches]

def validate_input_data(data: Dict[str, Any]) -> List[str]:
    """
    Validate input data and return list of errors.
    
    Args:
        data: Dictionary with input data
        
    Returns:
        List of error messages (empty if valid)
    """
    errors = []
    
    # Check required fields
    required_fields = ['title', 'source_type', 'identifier_type', 'identifier_value']
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: {field}")
    
    # Validate source type
    if 'source_type' in data and data['source_type'] not in VALID_SOURCE_TYPES:
        errors.append(f"Invalid source type: {data['source_type']}")
    
    # Validate identifier type
    if 'identifier_type' in data and data['identifier_type'] not in VALID_IDENTIFIER_TYPES:
        errors.append(f"Invalid identifier type: {data['identifier_type']}")
    
    # Validate URL if identifier type is URL
    if (data.get('identifier_type') == 'url' and 
        data.get('identifier_value') and 
        not validate_url(data['identifier_value'])):
        errors.append("Invalid URL format")
    
    return errors

def create_example_data() -> List[Dict[str, Any]]:
    """
    Create example data for testing and demonstrations.
    
    Returns:
        List of example source dictionaries
    """
    examples = [
        {
            'title': 'Attention Is All You Need',
            'source_type': 'paper',
            'identifier_type': 'arxiv',
            'identifier_value': '1706.03762',
            'notes': [
                {
                    'title': 'Key Innovation',
                    'content': 'Introduces the transformer architecture, eliminating the need for recurrence and convolutions.'
                }
            ]
        },
        {
            'title': 'Deep Learning',
            'source_type': 'book',
            'identifier_type': 'isbn',
            'identifier_value': '978-0262035613',
            'notes': [
                {
                    'title': 'Overview',
                    'content': 'Comprehensive textbook covering deep learning fundamentals and advanced topics.'
                }
            ]
        },
        {
            'title': 'The Illustrated Transformer',
            'source_type': 'blog',
            'identifier_type': 'url',
            'identifier_value': 'https://jalammar.github.io/illustrated-transformer/',
            'notes': [
                {
                    'title': 'Visual Explanation',
                    'content': 'Excellent visual explanation of how transformers work step by step.'
                }
            ]
        }
    ]
    
    return examples