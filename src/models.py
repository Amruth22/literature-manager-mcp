"""
Data Models and Constants for Literature Manager

This module defines the valid types and constants used throughout the system.
"""

from typing import Set, Dict, Any
from enum import Enum

class SourceType(Enum):
    """Valid source types for literature items."""
    PAPER = "paper"
    WEBPAGE = "webpage"
    BOOK = "book"
    VIDEO = "video"
    BLOG = "blog"
    
    @classmethod
    def all_values(cls) -> Set[str]:
        """Get all valid source type values."""
        return {item.value for item in cls}

class IdentifierType(Enum):
    """Valid identifier types for sources."""
    SEMANTIC_SCHOLAR = "semantic_scholar"
    ARXIV = "arxiv"
    DOI = "doi"
    ISBN = "isbn"
    URL = "url"
    
    @classmethod
    def all_values(cls) -> Set[str]:
        """Get all valid identifier type values."""
        return {item.value for item in cls}

class SourceStatus(Enum):
    """Valid status values for reading progress."""
    UNREAD = "unread"
    READING = "reading"
    COMPLETED = "completed"
    ARCHIVED = "archived"
    
    @classmethod
    def all_values(cls) -> Set[str]:
        """Get all valid status values."""
        return {item.value for item in cls}

class RelationType(Enum):
    """Valid relationship types between sources and entities."""
    DISCUSSES = "discusses"
    INTRODUCES = "introduces"
    EXTENDS = "extends"
    EVALUATES = "evaluates"
    APPLIES = "applies"
    CRITIQUES = "critiques"
    
    @classmethod
    def all_values(cls) -> Set[str]:
        """Get all valid relation type values."""
        return {item.value for item in cls}

# Helper dictionaries for validation
VALID_SOURCE_TYPES = SourceType.all_values()
VALID_IDENTIFIER_TYPES = IdentifierType.all_values()
VALID_STATUS_VALUES = SourceStatus.all_values()
VALID_RELATION_TYPES = RelationType.all_values()

def validate_source_type(source_type: str) -> bool:
    """Validate if source type is valid."""
    return source_type in VALID_SOURCE_TYPES

def validate_identifier_type(identifier_type: str) -> bool:
    """Validate if identifier type is valid."""
    return identifier_type in VALID_IDENTIFIER_TYPES

def validate_status(status: str) -> bool:
    """Validate if status is valid."""
    return status in VALID_STATUS_VALUES

def validate_relation_type(relation_type: str) -> bool:
    """Validate if relation type is valid."""
    return relation_type in VALID_RELATION_TYPES

# Example data structures for documentation
EXAMPLE_SOURCE = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Attention Is All You Need",
    "type": "paper",
    "status": "completed",
    "identifiers": {
        "arxiv": "1706.03762",
        "semantic_scholar": "204e3073870fae3d05bcbc2f6a8e263d9b72e776"
    },
    "notes": [
        {
            "title": "Key Insights",
            "content": "The transformer architecture eliminates recurrence...",
            "created_at": "2024-01-15T10:30:00"
        }
    ],
    "entity_links": [
        {
            "entity_name": "transformer architecture",
            "relation_type": "introduces",
            "notes": "First paper to introduce the transformer model"
        }
    ]
}

EXAMPLE_IDENTIFIERS = {
    "paper": {
        "arxiv": "1706.03762",
        "doi": "10.1000/xyz123",
        "semantic_scholar": "204e3073870fae3d05bcbc2f6a8e263d9b72e776"
    },
    "book": {
        "isbn": "978-0262035613",
        "url": "https://www.deeplearningbook.org/"
    },
    "webpage": {
        "url": "https://example.com/article"
    }
}