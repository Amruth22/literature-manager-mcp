"""
Database Operations for Literature Manager

This module handles all database interactions in a beginner-friendly way.
"""

import sqlite3
import json
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from contextlib import contextmanager

from .models import (
    validate_source_type, validate_identifier_type, 
    validate_status, validate_relation_type
)

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

@contextmanager
def get_db_connection(db_path: Path):
    """
    Context manager for database connections.
    
    Args:
        db_path: Path to the SQLite database file
        
    Yields:
        sqlite3.Connection: Database connection with row factory
    """
    if not db_path.exists():
        raise DatabaseError(f"Database not found at: {db_path}")
    
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
    finally:
        conn.close()

class LiteratureDatabase:
    """
    Main database class for literature management.
    
    This class provides simple methods for common database operations.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize the database connection.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = Path(db_path)
        if not self.db_path.exists():
            raise DatabaseError(f"Database not found at: {db_path}")
    
    def add_source(self, title: str, source_type: str, identifier_type: str, 
                   identifier_value: str) -> str:
        """
        Add a new source to the database.
        
        Args:
            title: Title of the source
            source_type: Type of source (paper, book, etc.)
            identifier_type: Type of identifier (arxiv, doi, etc.)
            identifier_value: Value of the identifier
            
        Returns:
            str: UUID of the created source
            
        Raises:
            DatabaseError: If validation fails or database error occurs
        """
        # Validate inputs
        if not validate_source_type(source_type):
            raise DatabaseError(f"Invalid source type: {source_type}")
        if not validate_identifier_type(identifier_type):
            raise DatabaseError(f"Invalid identifier type: {identifier_type}")
        
        # Check for existing source
        existing = self.find_source_by_identifier(identifier_type, identifier_value, source_type)
        if existing:
            raise DatabaseError(f"Source already exists with ID: {existing['id']}")
        
        # Create new source
        source_id = str(uuid.uuid4())
        identifiers = {identifier_type: identifier_value}
        
        with get_db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO sources (id, title, type, identifiers)
                    VALUES (?, ?, ?, ?)
                """, [source_id, title, source_type, json.dumps(identifiers)])
                conn.commit()
                return source_id
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to add source: {e}")
    
    def find_source_by_identifier(self, identifier_type: str, identifier_value: str, 
                                  source_type: str) -> Optional[Dict[str, Any]]:
        """
        Find a source by its identifier.
        
        Args:
            identifier_type: Type of identifier
            identifier_value: Value of the identifier
            source_type: Type of source
            
        Returns:
            Dict with source info if found, None otherwise
        """
        with get_db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, type, identifiers, status
                FROM sources
                WHERE type = ? AND json_extract(identifiers, ?) = ?
            """, [source_type, f"$.{identifier_type}", identifier_value])
            
            row = cursor.fetchone()
            if row:
                return {
                    'id': row['id'],
                    'title': row['title'],
                    'type': row['type'],
                    'identifiers': json.loads(row['identifiers']),
                    'status': row['status']
                }
            return None
    
    def get_source_by_id(self, source_id: str) -> Optional[Dict[str, Any]]:
        """
        Get complete source information by ID.
        
        Args:
            source_id: UUID of the source
            
        Returns:
            Dict with complete source info including notes and entity links
        """
        with get_db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get basic source info
            cursor.execute("""
                SELECT id, title, type, identifiers, status, created_at
                FROM sources WHERE id = ?
            """, [source_id])
            
            source_row = cursor.fetchone()
            if not source_row:
                return None
            
            source = {
                'id': source_row['id'],
                'title': source_row['title'],
                'type': source_row['type'],
                'identifiers': json.loads(source_row['identifiers']),
                'status': source_row['status'],
                'created_at': source_row['created_at']
            }
            
            # Get notes
            cursor.execute("""
                SELECT note_title, content, created_at
                FROM source_notes
                WHERE source_id = ?
                ORDER BY created_at DESC
            """, [source_id])
            
            source['notes'] = [
                {
                    'title': row['note_title'],
                    'content': row['content'],
                    'created_at': row['created_at']
                }
                for row in cursor.fetchall()
            ]
            
            # Get entity links
            cursor.execute("""
                SELECT entity_name, relation_type, notes, created_at
                FROM source_entity_links
                WHERE source_id = ?
            """, [source_id])
            
            source['entity_links'] = [
                {
                    'entity_name': row['entity_name'],
                    'relation_type': row['relation_type'],
                    'notes': row['notes'],
                    'created_at': row['created_at']
                }
                for row in cursor.fetchall()
            ]
            
            return source
    
    def add_note(self, source_id: str, note_title: str, content: str) -> bool:
        """
        Add a note to a source.
        
        Args:
            source_id: UUID of the source
            note_title: Title of the note
            content: Content of the note
            
        Returns:
            bool: True if successful
            
        Raises:
            DatabaseError: If source not found or database error
        """
        with get_db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if source exists
            cursor.execute("SELECT id FROM sources WHERE id = ?", [source_id])
            if not cursor.fetchone():
                raise DatabaseError(f"Source not found: {source_id}")
            
            # Check if note title already exists
            cursor.execute("""
                SELECT 1 FROM source_notes 
                WHERE source_id = ? AND note_title = ?
            """, [source_id, note_title])
            
            if cursor.fetchone():
                raise DatabaseError(f"Note with title '{note_title}' already exists")
            
            try:
                cursor.execute("""
                    INSERT INTO source_notes (source_id, note_title, content)
                    VALUES (?, ?, ?)
                """, [source_id, note_title, content])
                conn.commit()
                return True
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to add note: {e}")
    
    def update_status(self, source_id: str, new_status: str) -> bool:
        """
        Update the reading status of a source.
        
        Args:
            source_id: UUID of the source
            new_status: New status value
            
        Returns:
            bool: True if successful
            
        Raises:
            DatabaseError: If validation fails or database error
        """
        if not validate_status(new_status):
            raise DatabaseError(f"Invalid status: {new_status}")
        
        with get_db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    UPDATE sources SET status = ? WHERE id = ?
                """, [new_status, source_id])
                
                if cursor.rowcount == 0:
                    raise DatabaseError(f"Source not found: {source_id}")
                
                conn.commit()
                return True
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to update status: {e}")
    
    def link_to_entity(self, source_id: str, entity_name: str, 
                       relation_type: str, notes: Optional[str] = None) -> bool:
        """
        Link a source to an entity.
        
        Args:
            source_id: UUID of the source
            entity_name: Name of the entity
            relation_type: Type of relationship
            notes: Optional notes about the relationship
            
        Returns:
            bool: True if successful
            
        Raises:
            DatabaseError: If validation fails or database error
        """
        if not validate_relation_type(relation_type):
            raise DatabaseError(f"Invalid relation type: {relation_type}")
        
        with get_db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if source exists
            cursor.execute("SELECT id FROM sources WHERE id = ?", [source_id])
            if not cursor.fetchone():
                raise DatabaseError(f"Source not found: {source_id}")
            
            # Check if link already exists
            cursor.execute("""
                SELECT 1 FROM source_entity_links 
                WHERE source_id = ? AND entity_name = ?
            """, [source_id, entity_name])
            
            if cursor.fetchone():
                raise DatabaseError(f"Link already exists between source and entity '{entity_name}'")
            
            try:
                cursor.execute("""
                    INSERT INTO source_entity_links 
                    (source_id, entity_name, relation_type, notes)
                    VALUES (?, ?, ?, ?)
                """, [source_id, entity_name, relation_type, notes])
                conn.commit()
                return True
            except sqlite3.Error as e:
                raise DatabaseError(f"Failed to create entity link: {e}")
    
    def list_sources(self, source_type: Optional[str] = None, 
                     status: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        """
        List sources with optional filtering.
        
        Args:
            source_type: Optional filter by source type
            status: Optional filter by status
            limit: Maximum number of results
            
        Returns:
            List of source dictionaries
        """
        query = "SELECT id, title, type, status, created_at FROM sources"
        params = []
        conditions = []
        
        if source_type:
            if not validate_source_type(source_type):
                raise DatabaseError(f"Invalid source type: {source_type}")
            conditions.append("type = ?")
            params.append(source_type)
        
        if status:
            if not validate_status(status):
                raise DatabaseError(f"Invalid status: {status}")
            conditions.append("status = ?")
            params.append(status)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        
        with get_db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            return [
                {
                    'id': row['id'],
                    'title': row['title'],
                    'type': row['type'],
                    'status': row['status'],
                    'created_at': row['created_at']
                }
                for row in cursor.fetchall()
            ]
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            Dict with database statistics
        """
        with get_db_connection(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {}
            
            # Count sources by type
            cursor.execute("""
                SELECT type, COUNT(*) as count 
                FROM sources 
                GROUP BY type
            """)
            stats['sources_by_type'] = {row['type']: row['count'] for row in cursor.fetchall()}
            
            # Count sources by status
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM sources 
                GROUP BY status
            """)
            stats['sources_by_status'] = {row['status']: row['count'] for row in cursor.fetchall()}
            
            # Total counts
            cursor.execute("SELECT COUNT(*) as count FROM sources")
            stats['total_sources'] = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM source_notes")
            stats['total_notes'] = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM source_entity_links")
            stats['total_entity_links'] = cursor.fetchone()['count']
            
            return stats