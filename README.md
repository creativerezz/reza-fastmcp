# Dark Lavender Jellyfish MCP Server

A FastMCP-based Model Context Protocol (MCP) server providing text manipulation tools.

## Installation

### Prerequisites

We recommend using [uv](https://docs.astral.sh/uv/getting-started/installation/) to manage Python environments and dependencies.

### Install FastMCP

You can install FastMCP using uv or pip:

```bash
# Using uv (recommended)
uv add fastmcp

# Or using pip
pip install fastmcp
```

### Verify Installation

Verify FastMCP is installed correctly:

```bash
fastmcp version
```

You should see output like:
```
FastMCP version:                           2.11.3
MCP version:                               1.12.4
Python version:                            3.12.2
```

## Setup

1. **Install dependencies:**
   ```bash
   cd ~/mcp-servers/dark-lavender-jellyfish
   uv pip install fastmcp
   ```

2. **Make the server executable:**
   ```bash
   chmod +x server.py
   ```

3. **Test the server:**
   ```bash
   python server.py
   ```

## Available Tools

- **echo_tool**: Echo the input text
- **reverse_text**: Reverse the input text  
- **word_count**: Count words and characters in text
- **uppercase**: Convert text to uppercase
- **lowercase**: Convert text to lowercase

## Configuration for Claude Desktop

Add this configuration to your Claude Desktop settings:

```json
{
  "mcpServers": {
    "dark-lavender-jellyfish": {
      "command": "python",
      "args": ["~/mcp-servers/dark-lavender-jellyfish/server.py"]
    }
  }
}
```

## Upgrading from Official MCP SDK

If you're upgrading from the official MCP SDK's FastMCP 1.0 to FastMCP 2.0:

```python
# Before (MCP SDK 1.0)
# from mcp.server.fastmcp import FastMCP

# After (FastMCP 2.0+)
from fastmcp import FastMCP
```

## Development

To add new tools, edit `server.py` and add decorated functions:

```python
@mcp.tool()
def your_tool(param: str) -> str:
    """Your tool description"""
    return process(param)
```

## Versioning

For production use, always pin to exact versions:
```
fastmcp==2.11.0  # Good
fastmcp>=2.11.0  # Bad - may install breaking changes
```

## Contributing

See the [FastMCP Contributing Guide](https://github.com/jlowin/fastmcp) for details on:
- Setting up development environment
- Running tests and pre-commit hooks
- Submitting issues and pull requests
- Code standards and review process