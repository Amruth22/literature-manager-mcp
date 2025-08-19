# 📖 Examples and Use Cases

This document provides practical examples of how to use the Literature Manager MCP.

## Quick Start Examples

### Adding Your First Source

```python
# Add a research paper
add_source(
    title="Attention Is All You Need",
    source_type="paper",
    identifier_type="arxiv",
    identifier_value="1706.03762"
)
```

### Adding Different Types of Sources

```python
# Research paper
add_source("BERT: Pre-training of Deep Bidirectional Transformers", 
          "paper", "arxiv", "1810.04805")

# Book
add_source("Deep Learning", "book", "isbn", "978-0262035613")

# Website/Blog
add_source("The Illustrated Transformer", "webpage", "url", 
          "https://jalammar.github.io/illustrated-transformer/")

# Video
add_source("CS231n: Convolutional Neural Networks", "video", "url",
          "https://www.youtube.com/watch?v=OoUX-nOEjG0")
```

## Note-Taking Examples

### Basic Notes

```python
# Add a simple note
add_note("Attention Is All You Need", "paper", "arxiv", "1706.03762",
        "Key Insight", "Transformers eliminate the need for recurrence")
```

### Structured Notes

```python
# Add multiple structured notes
add_note("Deep Learning", "book", "isbn", "978-0262035613",
        "Chapter 1 Summary", "Introduction to machine learning concepts...")

add_note("Deep Learning", "book", "isbn", "978-0262035613",
        "Key Equations", "Gradient descent: θ = θ - α∇J(θ)")

add_note("Deep Learning", "book", "isbn", "978-0262035613",
        "Implementation Notes", "Code examples in Python using NumPy")
```

## Status Management Examples

### Tracking Reading Progress

```python
# Mark as currently reading
update_status("Attention Is All You Need", "paper", "arxiv", "1706.03762", "reading")

# Mark as completed
update_status("Attention Is All You Need", "paper", "arxiv", "1706.03762", "completed")

# Archive for later reference
update_status("Old Paper", "paper", "doi", "10.1000/xyz", "archived")
```

## Knowledge Graph Examples

### Linking Sources to Concepts

```python
# Link paper to the concept it introduces
link_to_entity("Attention Is All You Need", "paper", "arxiv", "1706.03762",
              "transformer architecture", "introduces",
              "First paper to introduce the transformer model")

# Link paper to concept it discusses
link_to_entity("BERT Paper", "paper", "arxiv", "1810.04805",
              "transformer architecture", "extends",
              "Builds on transformers for bidirectional understanding")

# Link book to broad concept
link_to_entity("Deep Learning", "book", "isbn", "978-0262035613",
              "neural networks", "discusses",
              "Comprehensive coverage of neural network architectures")
```

### Different Relationship Types

```python
# Paper that introduces a new concept
link_to_entity("Original Paper", "paper", "arxiv", "1234.5678",
              "new algorithm", "introduces")

# Paper that extends existing work
link_to_entity("Follow-up Paper", "paper", "arxiv", "2345.6789",
              "new algorithm", "extends")

# Paper that evaluates/compares approaches
link_to_entity("Survey Paper", "paper", "arxiv", "3456.7890",
              "new algorithm", "evaluates")

# Paper that applies concept to new domain
link_to_entity("Application Paper", "paper", "arxiv", "4567.8901",
              "new algorithm", "applies")

# Paper that critiques existing approach
link_to_entity("Critical Paper", "paper", "arxiv", "5678.9012",
              "new algorithm", "critiques")
```

## Search and Discovery Examples

### Finding Sources

```python
# List all sources
list_sources()

# Filter by type
list_sources(source_type="paper")

# Filter by status
list_sources(status="unread")

# Combine filters
list_sources(source_type="book", status="reading", limit=10)
```

### Searching by Title

```python
# Search for sources about transformers
search_sources("transformer")

# Search for deep learning resources
search_sources("deep learning", limit=5)
```

### Getting Detailed Information

```python
# Get complete details about a source
get_source_details("Attention Is All You Need", "paper", "arxiv", "1706.03762")
```

## Research Workflow Examples

### Literature Review Workflow

```python
# 1. Add sources as you discover them
add_source("Paper 1", "paper", "arxiv", "1111.1111")
add_source("Paper 2", "paper", "arxiv", "2222.2222")
add_source("Survey Paper", "paper", "arxiv", "3333.3333")

# 2. Mark papers you're currently reading
update_status("Paper 1", "paper", "arxiv", "1111.1111", "reading")

# 3. Take notes as you read
add_note("Paper 1", "paper", "arxiv", "1111.1111",
        "Main Contribution", "Introduces novel approach to...")
add_note("Paper 1", "paper", "arxiv", "1111.1111",
        "Limitations", "Doesn't handle edge cases...")

# 4. Connect to your knowledge graph
link_to_entity("Paper 1", "paper", "arxiv", "1111.1111",
              "machine learning", "applies")

# 5. Mark as completed when done
update_status("Paper 1", "paper", "arxiv", "1111.1111", "completed")
```

### Building a Knowledge Base

```python
# Start with foundational sources
add_source("Deep Learning Textbook", "book", "isbn", "978-0262035613")
link_to_entity("Deep Learning Textbook", "book", "isbn", "978-0262035613",
              "deep learning", "discusses")

# Add seminal papers
add_source("Attention Is All You Need", "paper", "arxiv", "1706.03762")
link_to_entity("Attention Is All You Need", "paper", "arxiv", "1706.03762",
              "transformer architecture", "introduces")

# Add recent developments
add_source("GPT-3 Paper", "paper", "arxiv", "2005.14165")
link_to_entity("GPT-3 Paper", "paper", "arxiv", "2005.14165",
              "transformer architecture", "extends")

# Add practical resources
add_source("Transformer Tutorial", "webpage", "url", "https://example.com/tutorial")
link_to_entity("Transformer Tutorial", "webpage", "url", "https://example.com/tutorial",
              "transformer architecture", "explains")
```

## Advanced Examples

### Batch Operations

For batch operations, you can use the database classes directly:

```python
from src.database import LiteratureDatabase

db = LiteratureDatabase("your_database.db")

# Add multiple sources
sources = [
    ("Paper 1", "paper", "arxiv", "1111.1111"),
    ("Paper 2", "paper", "arxiv", "2222.2222"),
    ("Paper 3", "paper", "arxiv", "3333.3333")
]

for title, source_type, id_type, id_value in sources:
    try:
        source_id = db.add_source(title, source_type, id_type, id_value)
        print(f"Added: {title}")
    except DatabaseError as e:
        print(f"Failed to add {title}: {e}")
```

### Data Analysis

```python
# Get database statistics
stats = database_stats()

# Analyze your reading habits
sources = list_sources(limit=1000)
completed = [s for s in sources['sources'] if s['status'] == 'completed']
print(f"Completion rate: {len(completed)}/{len(sources['sources'])}")
```

## Integration Examples

### With Claude Desktop

Once configured, you can use natural language with Claude:

```
"Add the BERT paper from arXiv 1810.04805 to my literature collection"

"Add a note to the Attention paper about the multi-head attention mechanism"

"Show me all the papers I haven't read yet"

"Link the GPT-3 paper to the concept of 'large language models' with relation 'introduces'"
```

### With Other Tools

The database is SQLite, so you can integrate with other tools:

```python
import sqlite3
import pandas as pd

# Export to CSV
conn = sqlite3.connect("literature.db")
df = pd.read_sql_query("SELECT * FROM sources", conn)
df.to_csv("my_literature.csv", index=False)

# Create visualizations
import matplotlib.pyplot as plt

# Plot sources by type
type_counts = df['type'].value_counts()
type_counts.plot(kind='bar')
plt.title('Sources by Type')
plt.show()
```

## Tips and Best Practices

### Consistent Naming

```python
# Use consistent entity names
link_to_entity(..., "transformer architecture", "introduces")  # Good
link_to_entity(..., "Transformer Architecture", "introduces")  # Inconsistent
link_to_entity(..., "transformers", "introduces")             # Inconsistent
```

### Meaningful Notes

```python
# Good: Specific and actionable
add_note(..., "Implementation Details", 
        "Uses 8 attention heads, 512 hidden dimensions, trained for 300k steps")

# Poor: Too vague
add_note(..., "Notes", "This is interesting")
```

### Structured Relationships

```python
# Build a hierarchy of concepts
link_to_entity("Attention Paper", ..., "attention mechanism", "introduces")
link_to_entity("BERT Paper", ..., "attention mechanism", "extends")
link_to_entity("Survey Paper", ..., "attention mechanism", "evaluates")
```

For more examples, see:
- [Basic Usage Examples](../examples/basic_usage.py)
- [Advanced Usage Examples](../examples/advanced_usage.py)