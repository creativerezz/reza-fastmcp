#!/usr/bin/env python3
"""
Dark Lavender Jellyfish MCP Server
A FastMCP-based Model Context Protocol server
"""

from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("Dark Lavender Jellyfish")

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

if __name__ == "__main__":
    mcp.run()