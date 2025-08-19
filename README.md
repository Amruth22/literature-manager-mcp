# 📚 Literature Manager MCP

A beginner-friendly system for managing research papers, books, and other sources using AI assistants through the Model Context Protocol (MCP).

## 🎯 What is this?

This tool helps you:
- **Organize** research papers, books, websites, and videos
- **Take notes** on your sources with structured titles
- **Track reading progress** (unread, reading, completed, archived)
- **Connect sources** to concepts in your knowledge base
- **Work with AI assistants** like Claude to manage your literature

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Basic familiarity with command line

### 2. Installation

```bash
# Clone this repository
git clone https://github.com/Amruth22/literature-manager-mcp.git
cd literature-manager-mcp

# Install dependencies
pip install -r requirements.txt

# Create your database
python setup_database.py
```

### 3. Choose Your Usage Method

#### Option A: Direct Python Usage (Recommended)

```bash
# Set your database path
## 📚 How to Use

### Command Line Interface

```bash
# Add a research paper
python cli.py add-source "Attention Is All You Need" paper arxiv 1706.03762

# Add a book
python cli.py add-source "Deep Learning" book isbn 978-0262035613

# Add a note
python cli.py add-note "Attention Is All You Need" paper arxiv 1706.03762 \
  "Key Insight" "Transformers eliminate recurrence"

# Update status
python cli.py update-status "Attention Is All You Need" paper arxiv 1706.03762 completed

# Link to entity
python cli.py link-entity "Attention Is All You Need" paper arxiv 1706.03762 \
  "transformer architecture" introduces

# List sources
python cli.py list --type paper --status unread

# Search sources
python cli.py search "transformer"

# Show statistics
python cli.py stats

# Get help
python cli.py help
```

### Direct Python Usage

```python
from src.database import LiteratureDatabase

# Initialize database
db = LiteratureDatabase("literature.db")

# Add a source
source_id = db.add_source(
    title="Attention Is All You Need",
    source_type="paper",
    identifier_type="arxiv",
    identifier_value="1706.03762"
)

    identifier_type="isbn",
    identifier_value="978-0262035613"
)

# Add a website
add_source(
    title="Understanding Transformers",
    source_type="webpage",
    identifier_type="url",
    identifier_value="https://example.com/transformers"
)
```

### Taking Notes

```python
# Add a note to a source
add_note(
    title="Attention Is All You Need",
    source_type="paper",
    identifier_type="arxiv",
    identifier_value="1706.03762",
    note_title="Key Insights",
    note_content="The transformer architecture eliminates recurrence..."
)
```

### Tracking Progress

```python
# Update reading status
update_status(
    title="Attention Is All You Need",
    source_type="paper",
    identifier_type="arxiv",
    identifier_value="1706.03762",
    new_status="completed"
)
```

### Connecting to Knowledge

```python
# Link a source to a concept
link_to_entity(
    title="Attention Is All You Need",
    source_type="paper",
    identifier_type="arxiv",
    identifier_value="1706.03762",
    entity_name="transformer architecture",
    relation_type="introduces"
)
```

## 🗂️ Source Types

- **paper**: Research papers, articles
- **book**: Books, textbooks
- **webpage**: Blog posts, websites
- **video**: YouTube videos, lectures
- **blog**: Blog posts, tutorials

## 🔗 Identifier Types

- **arxiv**: ArXiv paper IDs (e.g., "1706.03762")
- **doi**: Digital Object Identifiers
- **isbn**: Book ISBNs
- **url**: Web URLs
- **semantic_scholar**: Semantic Scholar paper IDs

## 📊 Reading Status

- **unread**: Haven't started reading
- **reading**: Currently reading
- **completed**: Finished reading
- **archived**: Saved for later reference

## 🔗 Relationship Types

When linking sources to concepts:

- **discusses**: Source talks about the concept
- **introduces**: Source first presents the concept
- **extends**: Source builds upon the concept
- **evaluates**: Source analyzes/critiques the concept
- **applies**: Source uses the concept practically
- **critiques**: Source criticizes the concept

## 🛠️ Available Commands

### Basic Operations
- `add_source()` - Add a new source
- `add_note()` - Add notes to sources
- `update_status()` - Change reading status
- `search_sources()` - Find sources

### Advanced Operations
- `link_to_entity()` - Connect sources to concepts
- `get_entity_sources()` - Find sources by concept
- `add_identifier()` - Add more IDs to existing sources

### Database Operations
- `list_sources()` - Show all sources
- `get_source_details()` - Get complete source info
- `database_stats()` - Show database statistics

## 📁 Project Structure

```
literature-manager-mcp/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── setup_database.py      # Database setup script
├── server.py             # Main MCP server
├── src/
│   ├── __init__.py
│   ├── database.py       # Database operations
│   ├── models.py         # Data models
│   ├── tools.py          # MCP tools
│   └── utils.py          # Helper functions
├── examples/
│   ├── basic_usage.py    # Simple examples
│   └── advanced_usage.py # Complex workflows
├── tests/
│   └── test_basic.py     # Unit tests
└── docs/
    ├── installation.md   # Detailed setup
    ├── examples.md       # More examples
    └── troubleshooting.md # Common issues
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Need Help?

- Check the [troubleshooting guide](docs/troubleshooting.md)
- Look at [examples](examples/)
- Open an [issue](https://github.com/Amruth22/literature-manager-mcp/issues)

## 🙏 Acknowledgments

- Based on the original work by [zongmin-yu](https://github.com/zongmin-yu/sqlite-literature-management-fastmcp-mcp-server)
- Built with [FastMCP](https://github.com/jlowin/fastmcp)
- Uses [Model Context Protocol](https://modelcontextprotocol.io/)