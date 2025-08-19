# 📦 Installation Guide

This guide will walk you through setting up the Literature Manager MCP step by step.

## Prerequisites

- **Python 3.8 or higher** - Check with `python --version`
- **Git** - For cloning the repository
- **Claude Desktop** (optional) - For AI assistant integration

## Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Amruth22/literature-manager-mcp.git

# Navigate to the directory
cd literature-manager-mcp
```

## Step 2: Install Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt
```

If you prefer using a virtual environment (recommended):

```bash
# Create virtual environment
python -m venv literature-env

# Activate it (Linux/Mac)
source literature-env/bin/activate

# Activate it (Windows)
literature-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Create Your Database

Run the setup script to create your literature database:

```bash
python setup_database.py
```

This will:
- Ask you where to create the database (default: `literature.db`)
- Create all necessary tables
- Set up indexes for better performance
- Show you the next steps

## Step 4: Set Environment Variable

Set the path to your database:

### Linux/Mac:
```bash
export LITERATURE_DB_PATH="/full/path/to/your/literature.db"

# To make it permanent, add to your ~/.bashrc or ~/.zshrc:
echo 'export LITERATURE_DB_PATH="/full/path/to/your/literature.db"' >> ~/.bashrc
```

### Windows:
```cmd
set LITERATURE_DB_PATH=C:\full\path\to\your\literature.db

# To make it permanent, use System Properties > Environment Variables
```

## Step 5: Test the Installation

Test that everything works:

```bash
# Run the example script
python examples/basic_usage.py

# Start the MCP server (Ctrl+C to stop)
python server.py
```

If you see "✅ Server ready for connections!" then everything is working!

## Step 6: Configure Claude Desktop (Optional)

To use with Claude Desktop, add this to your configuration file:

### Find your Claude Desktop config file:

- **Mac**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

### Add the server configuration:

```json
{
  "mcpServers": {
    "literature-manager": {
      "command": "python",
      "args": ["/full/path/to/literature-manager-mcp/server.py"],
      "env": {
        "LITERATURE_DB_PATH": "/full/path/to/your/literature.db"
      }
    }
  }
}
```

**Important**: Use full absolute paths, not relative paths like `~/` or `./`

### Restart Claude Desktop

After saving the configuration, restart Claude Desktop. You should see the Literature Manager tools available in your conversations.

## Troubleshooting

### Common Issues

#### 1. "LITERATURE_DB_PATH environment variable not set"

**Solution**: Make sure you've set the environment variable correctly:
```bash
echo $LITERATURE_DB_PATH  # Should show your database path
```

#### 2. "Database not found"

**Solution**: 
- Check that the database file exists at the specified path
- Run `python setup_database.py` if you haven't created it yet
- Use absolute paths, not relative ones

#### 3. "Module not found" errors

**Solution**:
- Make sure you've installed dependencies: `pip install -r requirements.txt`
- Check that you're in the correct directory
- If using virtual environment, make sure it's activated

#### 4. Claude Desktop doesn't show the tools

**Solution**:
- Check that the config file path is correct
- Use absolute paths in the configuration
- Restart Claude Desktop completely
- Check the Claude Desktop logs for errors

#### 5. Permission errors on Windows

**Solution**:
- Run command prompt as Administrator
- Or use PowerShell instead of Command Prompt

### Getting Help

If you're still having issues:

1. Check the [troubleshooting guide](troubleshooting.md)
2. Look at the [examples](../examples/) for working code
3. Open an [issue on GitHub](https://github.com/Amruth22/literature-manager-mcp/issues)

## Next Steps

Once installed, check out:

- [Basic Examples](../examples/basic_usage.py) - Learn the basics
- [Advanced Examples](../examples/advanced_usage.py) - Complex workflows
- [README](../README.md) - Full documentation

## Updating

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Restart your MCP server
```

Your database and configuration will be preserved during updates.