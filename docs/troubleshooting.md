# 🔧 Troubleshooting Guide

This guide helps you solve common issues with the Literature Manager MCP.

## Installation Issues

### Python Version Problems

**Problem**: "Python version not supported" or syntax errors

**Solution**:
```bash
# Check your Python version
python --version

# Should be 3.8 or higher. If not, install a newer version:
# - Visit https://python.org/downloads
# - Or use a version manager like pyenv
```

### Dependency Installation Fails

**Problem**: `pip install -r requirements.txt` fails

**Solutions**:
```bash
# Try upgrading pip first
pip install --upgrade pip

# Install dependencies one by one to identify the problem
pip install fastmcp
pip install pathlib

# If on Windows and getting compiler errors:
pip install --only-binary=all -r requirements.txt
```

### Virtual Environment Issues

**Problem**: Commands not found after creating virtual environment

**Solution**:
```bash
# Make sure you activated the environment
source literature-env/bin/activate  # Linux/Mac
# OR
literature-env\Scripts\activate     # Windows

# Verify activation (should show environment name in prompt)
which python  # Should point to virtual environment
```

## Database Issues

### Database Creation Fails

**Problem**: `python setup_database.py` fails with permission errors

**Solutions**:
```bash
# Check directory permissions
ls -la  # Linux/Mac
dir     # Windows

# Try creating in a different directory
python setup_database.py
# When prompted, enter: /tmp/literature.db (Linux/Mac)
# Or: C:\temp\literature.db (Windows)

# Make sure the directory exists
mkdir -p /path/to/database/directory
```

### Database Not Found

**Problem**: "Database not found at: /path/to/database"

**Solutions**:
```bash
# Check if file exists
ls -la /path/to/your/literature.db

# Check environment variable
echo $LITERATURE_DB_PATH

# Use absolute path
export LITERATURE_DB_PATH="/full/absolute/path/to/literature.db"

# Recreate database if needed
python setup_database.py
```

### Database Corruption

**Problem**: "Database disk image is malformed"

**Solutions**:
```bash
# Try to repair the database
sqlite3 literature.db ".recover" | sqlite3 literature_recovered.db

# Or recreate from scratch
mv literature.db literature.db.backup
python setup_database.py
```

## Server Issues

### Server Won't Start

**Problem**: `python server.py` fails immediately

**Solutions**:
```bash
# Check environment variable is set
echo $LITERATURE_DB_PATH

# Check database exists
ls -la $LITERATURE_DB_PATH

# Check for Python path issues
python -c "import sys; print(sys.path)"

# Run with verbose output
python -v server.py
```

### Import Errors

**Problem**: "ModuleNotFoundError: No module named 'src'"

**Solutions**:
```bash
# Make sure you're in the correct directory
pwd  # Should show literature-manager-mcp

# Check directory structure
ls -la src/

# Try running from project root
cd /path/to/literature-manager-mcp
python server.py
```

### Port Already in Use

**Problem**: "Address already in use" when starting server

**Solutions**:
```bash
# Find what's using the port
lsof -i :PORT_NUMBER  # Linux/Mac
netstat -ano | findstr :PORT_NUMBER  # Windows

# Kill the process or use a different port
# (FastMCP usually handles this automatically)
```

## Claude Desktop Integration Issues

### Configuration File Not Found

**Problem**: Can't find Claude Desktop config file

**Solutions**:
```bash
# Create the directory if it doesn't exist
mkdir -p ~/Library/Application\ Support/Claude  # Mac
mkdir -p %APPDATA%\Claude  # Windows

# Create empty config file
echo '{}' > ~/Library/Application\ Support/Claude/claude_desktop_config.json  # Mac
echo {} > %APPDATA%\Claude\claude_desktop_config.json  # Windows
```

### Tools Not Appearing in Claude

**Problem**: Literature Manager tools don't show up in Claude Desktop

**Solutions**:

1. **Check configuration syntax**:
   ```json
   {
     "mcpServers": {
       "literature-manager": {
         "command": "python",
         "args": ["/absolute/path/to/server.py"],
         "env": {
           "LITERATURE_DB_PATH": "/absolute/path/to/literature.db"
         }
       }
     }
   }
   ```

2. **Use absolute paths** (not `~/` or `./`):
   ```bash
   # Get absolute path
   realpath server.py
   realpath literature.db
   ```

3. **Check Claude Desktop logs**:
   - Mac: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`

4. **Restart Claude Desktop completely**:
   - Quit Claude Desktop
   - Wait 10 seconds
   - Restart Claude Desktop

### Permission Denied Errors

**Problem**: Claude Desktop can't execute the server

**Solutions**:
```bash
# Make server.py executable
chmod +x server.py

# Check Python path in config
which python  # Use this path in Claude config

# Try full Python path in config
{
  "command": "/usr/bin/python3",  # or wherever python is
  "args": ["/full/path/to/server.py"]
}
```

## Runtime Issues

### "Source already exists" Error

**Problem**: Can't add source that should be new

**Solutions**:
```bash
# Check for existing sources with same identifier
# Use the search function to find duplicates

# If it's a false positive, the source might have multiple identifiers
# Try using a different identifier type
```

### Slow Performance

**Problem**: Operations are very slow

**Solutions**:
```bash
# Vacuum the database to optimize
sqlite3 literature.db "VACUUM;"

# Check database size
ls -lh literature.db

# If very large, consider archiving old data
```

### Memory Issues

**Problem**: "Out of memory" errors

**Solutions**:
```bash
# Reduce batch sizes in operations
# Close other applications
# Check available memory: free -h (Linux), Activity Monitor (Mac), Task Manager (Windows)

# For large databases, consider pagination
```

## Data Issues

### Lost Data

**Problem**: Sources or notes disappeared

**Solutions**:
```bash
# Check if database file was moved or deleted
ls -la $LITERATURE_DB_PATH

# Look for backup files
ls -la *.db*

# Check database integrity
sqlite3 literature.db "PRAGMA integrity_check;"
```

### Encoding Issues

**Problem**: Special characters not displaying correctly

**Solutions**:
```bash
# Check database encoding
sqlite3 literature.db "PRAGMA encoding;"

# Should be UTF-8. If not, you may need to recreate the database
```

## Getting More Help

If these solutions don't work:

### 1. Enable Debug Mode

```bash
# Run with debug output
python -u server.py 2>&1 | tee debug.log
```

### 2. Check System Information

```bash
# Gather system info
python --version
pip list
uname -a  # Linux/Mac
systeminfo  # Windows
```

### 3. Create Minimal Test Case

```python
# Test basic functionality
from src.database import LiteratureDatabase
db = LiteratureDatabase("test.db")
# Try basic operations
```

### 4. Report Issues

When reporting issues, include:

- Operating system and version
- Python version
- Full error message
- Steps to reproduce
- Contents of debug.log

Open an issue at: https://github.com/Amruth22/literature-manager-mcp/issues

### 5. Community Help

- Check existing issues on GitHub
- Look at the examples for working code
- Ask questions in discussions

## Prevention Tips

### Regular Maintenance

```bash
# Backup your database regularly
cp literature.db literature_backup_$(date +%Y%m%d).db

# Vacuum database monthly
sqlite3 literature.db "VACUUM;"

# Update dependencies occasionally
pip install -r requirements.txt --upgrade
```

### Best Practices

1. **Always use absolute paths** in configurations
2. **Test changes** with the example script first
3. **Keep backups** of your database
4. **Use virtual environments** to avoid conflicts
5. **Check logs** when things go wrong