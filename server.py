#!/usr/bin/env python3
"""
Reza FastMCP Server
A FastMCP-based Model Context Protocol server with tools, resources, and prompts
"""

from fastmcp import FastMCP
from typing import List, Dict

# Initialize the FastMCP server
mcp = FastMCP("Reza FastMCP")

# ========== TOOLS ==========

@mcp.tool()
def echo_tool(text: str) -> str:
    """Echo the input text"""
    return text

@mcp.tool()
def reverse_text(text: str) -> str:
    """Reverse the input text"""
    return text[::-1]

@mcp.tool()
def word_count(text: str) -> dict:
    """Count words and characters in the input text"""
    words = text.split()
    return {
        "word_count": len(words),
        "character_count": len(text),
        "character_count_no_spaces": len(text.replace(" ", ""))
    }

@mcp.tool()
def uppercase(text: str) -> str:
    """Convert text to uppercase"""
    return text.upper()

@mcp.tool()
def lowercase(text: str) -> str:
    """Convert text to lowercase"""
    return text.lower()

@mcp.tool()
def split_text(text: str, delimiter: str = " ") -> List[str]:
    """Split text by a delimiter"""
    return text.split(delimiter)

@mcp.tool()
def join_text(parts: List[str], delimiter: str = " ") -> str:
    """Join text parts with a delimiter"""
    return delimiter.join(parts)

# ========== RESOURCES ==========

@mcp.resource("reza://info")
def reza_info() -> str:
    """Get information about the Reza FastMCP server"""
    return """
    Reza FastMCP Server
    ===================
    
    A FastMCP-powered text manipulation server providing:
    - Text transformation tools
    - Word and character analysis
    - Dynamic resource generation
    - Customizable prompts
    
    Version: 1.0.0
    Built with FastMCP 2.11.3
    """

@mcp.resource("reza://stats")
def server_stats() -> Dict:
    """Get server statistics"""
    return {
        "server_name": "Reza FastMCP",
        "version": "1.0.0",
        "available_tools": 7,
        "available_resources": 3,
        "available_prompts": 3
    }

@mcp.resource("reza://text/{operation}")
def text_operation_info(operation: str) -> str:
    """Get information about a specific text operation"""
    operations = {
        "reverse": "Reverses the order of characters in text",
        "uppercase": "Converts all characters to uppercase",
        "lowercase": "Converts all characters to lowercase",
        "count": "Counts words and characters in text",
        "split": "Splits text by a delimiter",
        "join": "Joins text parts with a delimiter"
    }
    return operations.get(operation, f"Unknown operation: {operation}")

# ========== PROMPTS ==========

@mcp.prompt("analyze_text")
def analyze_text_prompt(text: str) -> str:
    """Generate a prompt for analyzing text"""
    return f"""Please analyze the following text:

Text: {text}

Provide:
1. Word count
2. Character count
3. Most common words
4. Text complexity assessment
5. Suggested improvements
"""

@mcp.prompt("transform_text")
def transform_text_prompt(text: str, transformation: str) -> str:
    """Generate a prompt for transforming text"""
    return f"""Transform the following text using {transformation}:

Original text: {text}

Apply the {transformation} transformation and explain the result.
"""

@mcp.prompt("creative_writing")
def creative_writing_prompt(theme: str, style: str = "narrative") -> str:
    """Generate a creative writing prompt"""
    return f"""Create a {style} piece with the following theme:

Theme: {theme}
Style: {style}

Requirements:
- Be creative and original
- Use vivid descriptions
- Include engaging dialogue if appropriate
- Aim for approximately 300-500 words
"""

if __name__ == "__main__":
    mcp.run()