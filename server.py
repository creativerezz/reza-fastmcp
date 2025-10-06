#!/usr/bin/env python3
"""
Reza FastMCP Server
A FastMCP-based Model Context Protocol server with tools, resources, and prompts
"""

from fastmcp import FastMCP
from typing import List, Dict, Any
import re
import json
import base64
import hashlib
import uuid
import datetime

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

@mcp.tool()
def title_case(text: str) -> str:
    """Convert text to title case"""
    return text.title()

@mcp.tool()
def capitalize_first(text: str) -> str:
    """Capitalize only the first letter of text"""
    return text.capitalize()

@mcp.tool()
def remove_whitespace(text: str) -> str:
    """Remove all whitespace from text"""
    return re.sub(r'\s+', '', text)

@mcp.tool()
def normalize_whitespace(text: str) -> str:
    """Normalize whitespace (replace multiple spaces with single space)"""
    return re.sub(r'\s+', ' ', text.strip())

@mcp.tool()
def extract_emails(text: str) -> List[str]:
    """Extract email addresses from text"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, text)

@mcp.tool()
def extract_urls(text: str) -> List[str]:
    """Extract URLs from text"""
    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return re.findall(url_pattern, text)

@mcp.tool()
def extract_phone_numbers(text: str) -> List[str]:
    """Extract phone numbers from text"""
    phone_pattern = r'(\+?1-?)?(\(?[0-9]{3}\)?[-.\s]?)?[0-9]{3}[-.\s]?[0-9]{4}'
    return re.findall(phone_pattern, text)

@mcp.tool()
def slug_from_text(text: str) -> str:
    """Create a URL-friendly slug from text"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')

@mcp.tool()
def encode_base64(text: str) -> str:
    """Encode text to base64"""
    return base64.b64encode(text.encode('utf-8')).decode('utf-8')

@mcp.tool()
def decode_base64(encoded_text: str) -> str:
    """Decode base64 text"""
    try:
        return base64.b64decode(encoded_text).decode('utf-8')
    except Exception as e:
        return f"Error decoding base64: {str(e)}"

@mcp.tool()
def hash_text(text: str, algorithm: str = "sha256") -> str:
    """Generate hash of text using specified algorithm (md5, sha1, sha256, sha512)"""
    algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512
    }
    
    if algorithm not in algorithms:
        return f"Unsupported algorithm. Choose from: {', '.join(algorithms.keys())}"
    
    hash_func = algorithms[algorithm]
    return hash_func(text.encode('utf-8')).hexdigest()

@mcp.tool()
def generate_uuid() -> str:
    """Generate a random UUID"""
    return str(uuid.uuid4())

@mcp.tool()
def generate_password(length: int = 12, include_symbols: bool = True) -> str:
    """Generate a secure random password"""
    import string
    import secrets
    
    chars = string.ascii_letters + string.digits
    if include_symbols:
        chars += "!@#$%^&*"
    
    return ''.join(secrets.choice(chars) for _ in range(length))

@mcp.tool()
def format_json(json_string: str, indent: int = 2) -> str:
    """Format JSON string with proper indentation"""
    try:
        parsed = json.loads(json_string)
        return json.dumps(parsed, indent=indent, ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {str(e)}"

@mcp.tool()
def minify_json(json_string: str) -> str:
    """Minify JSON string (remove whitespace)"""
    try:
        parsed = json.loads(json_string)
        return json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
    except json.JSONDecodeError as e:
        return f"Invalid JSON: {str(e)}"

@mcp.tool()
def current_timestamp() -> Dict[str, Any]:
    """Get current timestamp in various formats"""
    now = datetime.datetime.now()
    utc_now = datetime.datetime.utcnow()
    
    return {
        "unix_timestamp": int(now.timestamp()),
        "iso_format": now.isoformat(),
        "utc_iso": utc_now.isoformat() + "Z",
        "human_readable": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date_only": now.strftime("%Y-%m-%d"),
        "time_only": now.strftime("%H:%M:%S")
    }

@mcp.tool()
def text_statistics(text: str) -> Dict[str, Any]:
    """Get comprehensive text statistics"""
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    return {
        "character_count": len(text),
        "character_count_no_spaces": len(text.replace(" ", "")),
        "word_count": len(words),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
        "average_sentence_length": len(words) / len(sentences) if sentences else 0,
        "unique_words": len(set(word.lower() for word in words)),
        "reading_time_minutes": len(words) / 200  # Average reading speed
    }

@mcp.tool()
def find_and_replace(text: str, find: str, replace: str, case_sensitive: bool = True) -> str:
    """Find and replace text with options"""
    flags = 0 if case_sensitive else re.IGNORECASE
    return re.sub(re.escape(find), replace, text, flags=flags)

@mcp.tool()
def sort_lines(text: str, reverse: bool = False, case_sensitive: bool = True) -> str:
    """Sort lines in text"""
    lines = text.split('\n')
    if case_sensitive:
        lines.sort(reverse=reverse)
    else:
        lines.sort(key=str.lower, reverse=reverse)
    return '\n'.join(lines)

@mcp.tool()
def remove_duplicates(text: str, preserve_order: bool = True) -> str:
    """Remove duplicate lines from text"""
    lines = text.split('\n')
    if preserve_order:
        seen = set()
        unique_lines = []
        for line in lines:
            if line not in seen:
                seen.add(line)
                unique_lines.append(line)
        return '\n'.join(unique_lines)
    else:
        return '\n'.join(list(set(lines)))

@mcp.tool()
def word_frequency(text: str, top_n: int = 10) -> Dict[str, int]:
    """Get word frequency count"""
    words = re.findall(r'\b\w+\b', text.lower())
    from collections import Counter
    word_counts = Counter(words)
    return dict(word_counts.most_common(top_n))

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
        "available_tools": 28,
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
        "title_case": "Converts text to title case",
        "capitalize_first": "Capitalizes only the first letter",
        "count": "Counts words and characters in text",
        "split": "Splits text by a delimiter",
        "join": "Joins text parts with a delimiter",
        "normalize_whitespace": "Normalizes whitespace in text",
        "remove_whitespace": "Removes all whitespace from text",
        "extract_emails": "Extracts email addresses from text",
        "extract_urls": "Extracts URLs from text",
        "extract_phone_numbers": "Extracts phone numbers from text",
        "slug": "Creates URL-friendly slug from text",
        "base64_encode": "Encodes text to base64",
        "base64_decode": "Decodes base64 text",
        "hash": "Generates hash of text (md5, sha1, sha256, sha512)",
        "statistics": "Gets comprehensive text statistics",
        "find_replace": "Find and replace text with options",
        "sort_lines": "Sort lines in text",
        "remove_duplicates": "Remove duplicate lines",
        "word_frequency": "Get word frequency analysis"
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