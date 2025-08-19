#!/usr/bin/env python3
"""
Basic Unit Tests for Literature Manager

These tests verify that the core functionality works correctly.
Run with: python -m pytest tests/test_basic.py
"""

import unittest
import tempfile
import os
import sqlite3
import json
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.database import LiteratureDatabase, DatabaseError
from src.models import VALID_SOURCE_TYPES, VALID_IDENTIFIER_TYPES
from src.utils import clean_title, extract_arxiv_id, validate_url

class TestDatabase(unittest.TestCase):
    """Test database operations."""
    
    def setUp(self):
        """Set up test database for each test."""
        # Create temporary database
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        
        # Create database schema
        self._create_test_database()
        
        # Initialize database instance
        self.db = LiteratureDatabase(self.db_path)
    
    def tearDown(self):
        """Clean up after each test."""
        # Remove temporary database
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def _create_test_database(self):
        """Create test database with schema."""
        with sqlite3.connect(self.db_path) as conn:
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
    
    def test_add_source_success(self):
        """Test successful source addition."""
        source_id = self.db.add_source(
            title="Test Paper",
            source_type="paper",
            identifier_type="arxiv",
            identifier_value="1234.5678"
        )
        
        self.assertIsInstance(source_id, str)
        self.assertEqual(len(source_id), 36)  # UUID length
        
        # Verify source was added
        source = self.db.get_source_by_id(source_id)
        self.assertIsNotNone(source)
        self.assertEqual(source['title'], "Test Paper")
        self.assertEqual(source['type'], "paper")
        self.assertEqual(source['identifiers']['arxiv'], "1234.5678")
    
    def test_add_source_invalid_type(self):
        """Test adding source with invalid type."""
        with self.assertRaises(DatabaseError):
            self.db.add_source(
                title="Test",
                source_type="invalid_type",
                identifier_type="arxiv",
                identifier_value="1234.5678"
            )
    
    def test_add_source_duplicate(self):
        """Test adding duplicate source."""
        # Add first source
        self.db.add_source(
            title="Test Paper",
            source_type="paper",
            identifier_type="arxiv",
            identifier_value="1234.5678"
        )
        
        # Try to add duplicate
        with self.assertRaises(DatabaseError):
            self.db.add_source(
                title="Test Paper Duplicate",
                source_type="paper",
                identifier_type="arxiv",
                identifier_value="1234.5678"
            )
    
    def test_find_source_by_identifier(self):
        """Test finding source by identifier."""
        # Add source
        source_id = self.db.add_source(
            title="Test Paper",
            source_type="paper",
            identifier_type="arxiv",
            identifier_value="1234.5678"
        )
        
        # Find by identifier
        found = self.db.find_source_by_identifier("arxiv", "1234.5678", "paper")
        self.assertIsNotNone(found)
        self.assertEqual(found['id'], source_id)
        self.assertEqual(found['title'], "Test Paper")
        
        # Try non-existent identifier
        not_found = self.db.find_source_by_identifier("arxiv", "9999.9999", "paper")
        self.assertIsNone(not_found)
    
    def test_add_note_success(self):
        """Test successful note addition."""
        # Add source
        source_id = self.db.add_source(
            title="Test Paper",
            source_type="paper",
            identifier_type="arxiv",
            identifier_value="1234.5678"
        )
        
        # Add note
        result = self.db.add_note(source_id, "Test Note", "This is a test note")
        self.assertTrue(result)
        
        # Verify note was added
        source = self.db.get_source_by_id(source_id)
        self.assertEqual(len(source['notes']), 1)
        self.assertEqual(source['notes'][0]['title'], "Test Note")
        self.assertEqual(source['notes'][0]['content'], "This is a test note")
    
    def test_add_note_duplicate_title(self):
        """Test adding note with duplicate title."""
        # Add source
        source_id = self.db.add_source(
            title="Test Paper",
            source_type="paper",
            identifier_type="arxiv",
            identifier_value="1234.5678"
        )
        
        # Add first note
        self.db.add_note(source_id, "Test Note", "First note")
        
        # Try to add note with same title
        with self.assertRaises(DatabaseError):
            self.db.add_note(source_id, "Test Note", "Second note")
    
    def test_update_status(self):
        """Test status update."""
        # Add source
        source_id = self.db.add_source(
            title="Test Paper",
            source_type="paper",
            identifier_type="arxiv",
            identifier_value="1234.5678"
        )
        
        # Update status
        result = self.db.update_status(source_id, "completed")
        self.assertTrue(result)
        
        # Verify status was updated
        source = self.db.get_source_by_id(source_id)
        self.assertEqual(source['status'], "completed")
    
    def test_update_status_invalid(self):
        """Test updating to invalid status."""
        # Add source
        source_id = self.db.add_source(
            title="Test Paper",
            source_type="paper",
            identifier_type="arxiv",
            identifier_value="1234.5678"
        )
        
        # Try invalid status
        with self.assertRaises(DatabaseError):
            self.db.update_status(source_id, "invalid_status")
    
    def test_link_to_entity(self):
        """Test entity linking."""
        # Add source
        source_id = self.db.add_source(
            title="Test Paper",
            source_type="paper",
            identifier_type="arxiv",
            identifier_value="1234.5678"
        )
        
        # Link to entity
        result = self.db.link_to_entity(
            source_id, 
            "test concept", 
            "discusses", 
            "Test relationship"
        )
        self.assertTrue(result)
        
        # Verify link was created
        source = self.db.get_source_by_id(source_id)
        self.assertEqual(len(source['entity_links']), 1)
        self.assertEqual(source['entity_links'][0]['entity_name'], "test concept")
        self.assertEqual(source['entity_links'][0]['relation_type'], "discusses")
    
    def test_list_sources(self):
        """Test listing sources."""
        # Add multiple sources
        self.db.add_source("Paper 1", "paper", "arxiv", "1111.1111")
        self.db.add_source("Book 1", "book", "isbn", "978-1111111111")
        self.db.add_source("Paper 2", "paper", "arxiv", "2222.2222")
        
        # List all sources
        all_sources = self.db.list_sources()
        self.assertEqual(len(all_sources), 3)
        
        # List only papers
        papers = self.db.list_sources(source_type="paper")
        self.assertEqual(len(papers), 2)
        
        # List with limit
        limited = self.db.list_sources(limit=2)
        self.assertEqual(len(limited), 2)
    
    def test_database_stats(self):
        """Test database statistics."""
        # Add some test data
        source_id = self.db.add_source("Test Paper", "paper", "arxiv", "1234.5678")
        self.db.add_note(source_id, "Note 1", "Content 1")
        self.db.link_to_entity(source_id, "concept", "discusses")
        
        # Get stats
        stats = self.db.get_database_stats()
        
        self.assertEqual(stats['total_sources'], 1)
        self.assertEqual(stats['total_notes'], 1)
        self.assertEqual(stats['total_entity_links'], 1)
        self.assertIn('paper', stats['sources_by_type'])
        self.assertEqual(stats['sources_by_type']['paper'], 1)

class TestUtils(unittest.TestCase):
    """Test utility functions."""
    
    def test_clean_title(self):
        """Test title cleaning."""
        self.assertEqual(clean_title("  The  Title  "), "Title")
        self.assertEqual(clean_title("A Great Paper"), "Great Paper")
        self.assertEqual(clean_title("An Important Book"), "Important Book")
        self.assertEqual(clean_title("Normal Title"), "Normal Title")
    
    def test_extract_arxiv_id(self):
        """Test arXiv ID extraction."""
        # New format
        self.assertEqual(extract_arxiv_id("arxiv:1706.03762"), "1706.03762")
        self.assertEqual(extract_arxiv_id("1706.03762v1"), "1706.03762v1")
        self.assertEqual(extract_arxiv_id("https://arxiv.org/abs/1706.03762"), "1706.03762")
        
        # Old format
        self.assertEqual(extract_arxiv_id("math.CO/0123456"), "math.CO/0123456")
        
        # No match
        self.assertIsNone(extract_arxiv_id("not an arxiv id"))
    
    def test_validate_url(self):
        """Test URL validation."""
        # Valid URLs
        self.assertTrue(validate_url("https://example.com"))
        self.assertTrue(validate_url("http://example.com/path"))
        self.assertTrue(validate_url("https://sub.example.com:8080/path?query=1"))
        
        # Invalid URLs
        self.assertFalse(validate_url("not a url"))
        self.assertFalse(validate_url("ftp://example.com"))
        self.assertFalse(validate_url("example.com"))

class TestModels(unittest.TestCase):
    """Test data models and validation."""
    
    def test_valid_types(self):
        """Test that valid type sets are not empty."""
        self.assertGreater(len(VALID_SOURCE_TYPES), 0)
        self.assertGreater(len(VALID_IDENTIFIER_TYPES), 0)
        
        # Check specific values
        self.assertIn("paper", VALID_SOURCE_TYPES)
        self.assertIn("arxiv", VALID_IDENTIFIER_TYPES)

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)