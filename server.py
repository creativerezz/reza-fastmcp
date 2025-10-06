#!/usr/bin/env python3
"""
Reza FastMCP Server
A FastMCP-based Model Context Protocol server with tools, resources, and prompts
"""

from fastmcp import FastMCP
from typing import List, Dict, Any, Optional
import re
import json
import base64
import hashlib
import uuid
import datetime
from collections import Counter
import string
import secrets
import os
import glob
import pathlib
from pathlib import Path
import csv
import io
import math
import statistics
import subprocess

# Import new libraries
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

try:
    import validators
    VALIDATORS_AVAILABLE = True
except ImportError:
    VALIDATORS_AVAILABLE = False

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

try:
    from dateutil import parser as date_parser
    import pytz
    DATEUTIL_AVAILABLE = True
except ImportError:
    DATEUTIL_AVAILABLE = False

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
    word_counts = Counter(words)
    return dict(word_counts.most_common(top_n))

# ========== File System Tools ==========

@mcp.tool()
def create_file(file_path: str, content: str, encoding: str = "utf-8") -> Dict[str, Any]:
    """Create a new file with specified content"""
    try:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
        
        return {
            "success": True,
            "file_path": str(path.absolute()),
            "size_bytes": len(content.encode(encoding)),
            "encoding": encoding
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def read_file(file_path: str, encoding: str = "utf-8", max_lines: int = None) -> Dict[str, Any]:
    """Read file content with optional line limit"""
    try:
        path = Path(file_path)
        if not path.exists():
            return {"error": "File not found"}
        
        with open(path, 'r', encoding=encoding) as f:
            if max_lines:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        break
                    lines.append(line.rstrip('\n'))
                content = '\n'.join(lines)
                truncated = True
            else:
                content = f.read()
                truncated = False
        
        return {
            "file_path": str(path.absolute()),
            "content": content,
            "size_bytes": path.stat().st_size,
            "encoding": encoding,
            "truncated": truncated,
            "lines_read": len(content.split('\n')) if content else 0
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def list_directory(dir_path: str = ".", show_hidden: bool = False, recursive: bool = False) -> Dict[str, Any]:
    """List directory contents"""
    try:
        path = Path(dir_path)
        if not path.exists():
            return {"error": "Directory not found"}
        if not path.is_dir():
            return {"error": "Path is not a directory"}
        
        files = []
        directories = []
        
        if recursive:
            pattern = "**/*" if show_hidden else "**/[!.]*"
            for item in path.glob(pattern):
                if item.is_file():
                    files.append({
                        "name": item.name,
                        "path": str(item.relative_to(path)),
                        "size": item.stat().st_size,
                        "modified": datetime.datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                    })
                elif item.is_dir():
                    directories.append({
                        "name": item.name,
                        "path": str(item.relative_to(path))
                    })
        else:
            for item in path.iterdir():
                if not show_hidden and item.name.startswith('.'):
                    continue
                
                if item.is_file():
                    files.append({
                        "name": item.name,
                        "path": str(item.relative_to(path)),
                        "size": item.stat().st_size,
                        "modified": datetime.datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                    })
                elif item.is_dir():
                    directories.append({
                        "name": item.name,
                        "path": str(item.relative_to(path))
                    })
        
        return {
            "directory": str(path.absolute()),
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_directories": len(directories)
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def file_info(file_path: str) -> Dict[str, Any]:
    """Get detailed file information"""
    try:
        path = Path(file_path)
        if not path.exists():
            return {"error": "File not found"}
        
        stat = path.stat()
        return {
            "path": str(path.absolute()),
            "name": path.name,
            "extension": path.suffix,
            "size_bytes": stat.st_size,
            "size_human": _format_file_size(stat.st_size),
            "is_file": path.is_file(),
            "is_directory": path.is_dir(),
            "created": datetime.datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "accessed": datetime.datetime.fromtimestamp(stat.st_atime).isoformat(),
            "permissions": oct(stat.st_mode)[-3:]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def search_files(directory: str = ".", pattern: str = "*", content_search: str = None, case_sensitive: bool = False) -> List[Dict[str, Any]]:
    """Search for files by name pattern and/or content"""
    try:
        path = Path(directory)
        if not path.exists():
            return [{"error": "Directory not found"}]
        
        results = []
        
        # Search by filename pattern
        for file_path in path.rglob(pattern):
            if file_path.is_file():
                result = {
                    "path": str(file_path.absolute()),
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "modified": datetime.datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                }
                
                # If content search is specified, search within the file
                if content_search:
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            search_text = content_search if case_sensitive else content_search.lower()
                            file_content = content if case_sensitive else content.lower()
                            
                            if search_text in file_content:
                                # Find line numbers where the search term appears
                                lines = content.split('\n')
                                matching_lines = []
                                for i, line in enumerate(lines):
                                    line_to_search = line if case_sensitive else line.lower()
                                    if search_text in line_to_search:
                                        matching_lines.append({
                                            "line_number": i + 1,
                                            "content": line.strip()
                                        })
                                
                                result["matches"] = matching_lines[:10]  # Limit to first 10 matches
                                results.append(result)
                    except Exception:
                        # Skip files that can't be read as text
                        continue
                else:
                    results.append(result)
        
        return results
    except Exception as e:
        return [{"error": str(e)}]

def _format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"

# ========== YouTube Tools ==========

@mcp.tool()
def youtube_transcript(url: str, language: str = "en") -> Dict[str, Any]:
    """Get YouTube video transcript"""
    if not YOUTUBE_AVAILABLE:
        return {"error": "youtube-transcript-api not installed"}
    
    try:
        # Extract video ID from URL
        video_id = None
        if "youtube.com/watch?v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        else:
            return {"error": "Invalid YouTube URL"}
        
        # Get transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        
        # Format transcript
        formatter = TextFormatter()
        text_formatted = formatter.format_transcript(transcript_list)
        
        # Calculate duration
        total_duration = transcript_list[-1]["start"] + transcript_list[-1]["duration"] if transcript_list else 0
        
        return {
            "video_id": video_id,
            "language": language,
            "transcript": text_formatted,
            "segments": len(transcript_list),
            "duration_seconds": total_duration,
            "duration_formatted": str(datetime.timedelta(seconds=int(total_duration)))
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def youtube_transcript_with_timestamps(url: str, language: str = "en") -> List[Dict[str, Any]]:
    """Get YouTube video transcript with timestamps"""
    if not YOUTUBE_AVAILABLE:
        return [{"error": "youtube-transcript-api not installed"}]
    
    try:
        # Extract video ID from URL
        video_id = None
        if "youtube.com/watch?v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        else:
            return [{"error": "Invalid YouTube URL"}]
        
        # Get transcript
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])
        
        # Format with timestamps
        formatted = []
        for entry in transcript_list:
            formatted.append({
                "time": str(datetime.timedelta(seconds=int(entry["start"]))),
                "text": entry["text"],
                "duration": entry["duration"]
            })
        
        return formatted
    except Exception as e:
        return [{"error": str(e)}]

# ========== Web Tools ==========

@mcp.tool()
def fetch_webpage(url: str) -> Dict[str, Any]:
    """Fetch and parse webpage content"""
    if not REQUESTS_AVAILABLE or not BS4_AVAILABLE:
        return {"error": "requests or beautifulsoup4 not installed"}
    
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content
        text = soup.get_text(separator='\n', strip=True)
        
        # Extract metadata
        title = soup.title.string if soup.title else None
        description = None
        if soup.find('meta', attrs={'name': 'description'}):
            description = soup.find('meta', attrs={'name': 'description'}).get('content')
        
        return {
            "url": url,
            "status_code": response.status_code,
            "title": title,
            "description": description,
            "text_length": len(text),
            "text": text[:5000],  # First 5000 chars
            "links_count": len(soup.find_all('a')),
            "images_count": len(soup.find_all('img'))
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def extract_links(url: str) -> List[str]:
    """Extract all links from a webpage"""
    if not REQUESTS_AVAILABLE or not BS4_AVAILABLE:
        return ["Error: requests or beautifulsoup4 not installed"]
    
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Convert relative URLs to absolute
            if href.startswith('http'):
                links.append(href)
            elif href.startswith('/'):
                from urllib.parse import urljoin
                links.append(urljoin(url, href))
        
        return list(set(links))  # Remove duplicates
    except Exception as e:
        return [f"Error: {str(e)}"]

# ========== Network/API Tools ==========

@mcp.tool()
def http_request(url: str, method: str = "GET", headers: Dict[str, str] = None, data: str = None, timeout: int = 10) -> Dict[str, Any]:
    """Make HTTP request with custom method, headers, and data"""
    if not REQUESTS_AVAILABLE:
        return {"error": "requests library not installed"}
    
    try:
        method = method.upper()
        headers = headers or {}
        
        # Add default headers
        if 'User-Agent' not in headers:
            headers['User-Agent'] = 'FastMCP-Server/1.0'
        
        # Parse JSON data if provided
        json_data = None
        if data:
            try:
                json_data = json.loads(data)
                if 'Content-Type' not in headers:
                    headers['Content-Type'] = 'application/json'
            except json.JSONDecodeError:
                # If not JSON, send as raw data
                pass
        
        # Make request
        if json_data:
            response = requests.request(method, url, headers=headers, json=json_data, timeout=timeout)
        elif data:
            response = requests.request(method, url, headers=headers, data=data, timeout=timeout)
        else:
            response = requests.request(method, url, headers=headers, timeout=timeout)
        
        # Parse response
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            response_json = None
        
        return {
            "url": url,
            "method": method,
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "response_time_ms": int(response.elapsed.total_seconds() * 1000),
            "json": response_json,
            "text": response.text[:5000] if response_json is None else None,  # First 5000 chars if not JSON
            "size_bytes": len(response.content)
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def ping_host(host: str, count: int = 4) -> Dict[str, Any]:
    """Ping a host to check connectivity"""
    try:
        import platform
        
        # Determine ping command based on OS
        system = platform.system().lower()
        if system == "windows":
            cmd = ["ping", "-n", str(count), host]
        else:
            cmd = ["ping", "-c", str(count), host]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        return {
            "host": host,
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def test_api_endpoint(url: str, expected_status: int = 200, timeout: int = 10) -> Dict[str, Any]:
    """Test an API endpoint and validate response"""
    if not REQUESTS_AVAILABLE:
        return {"error": "requests library not installed"}
    
    try:
        start_time = datetime.datetime.now()
        response = requests.get(url, timeout=timeout)
        end_time = datetime.datetime.now()
        
        response_time = (end_time - start_time).total_seconds() * 1000
        
        # Basic health checks
        status_ok = response.status_code == expected_status
        has_content = len(response.content) > 0
        
        # Try to parse as JSON
        is_json = False
        json_valid = False
        try:
            response.json()
            is_json = True
            json_valid = True
        except json.JSONDecodeError:
            is_json = response.headers.get('content-type', '').startswith('application/json')
            json_valid = False
        
        return {
            "url": url,
            "status_code": response.status_code,
            "expected_status": expected_status,
            "status_ok": status_ok,
            "response_time_ms": int(response_time),
            "has_content": has_content,
            "content_length": len(response.content),
            "content_type": response.headers.get('content-type'),
            "is_json": is_json,
            "json_valid": json_valid,
            "headers": dict(response.headers),
            "overall_health": status_ok and has_content and (not is_json or json_valid)
        }
    except Exception as e:
        return {"error": str(e)}

# ========== System Tools ==========

@mcp.tool()
def system_info() -> Dict[str, Any]:
    """Get system information"""
    try:
        import platform
        import psutil
        
        # CPU info
        cpu_count = psutil.cpu_count()
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Memory info
        memory = psutil.virtual_memory()
        
        # Disk info
        disk = psutil.disk_usage('/')
        
        return {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version()
            },
            "cpu": {
                "count": cpu_count,
                "usage_percent": cpu_usage
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "usage_percent": memory.percent
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "usage_percent": round((disk.used / disk.total) * 100, 1)
            }
        }
    except ImportError:
        # Fallback without psutil
        import platform
        return {
            "platform": {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python_version": platform.python_version()
            },
            "note": "Install psutil for detailed system metrics"
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_environment_variable(name: str, default: str = None) -> str:
    """Get environment variable value"""
    return os.environ.get(name, default)

@mcp.tool()
def list_environment_variables(filter_pattern: str = None) -> Dict[str, str]:
    """List environment variables, optionally filtered by pattern"""
    try:
        env_vars = dict(os.environ)
        
        if filter_pattern:
            import fnmatch
            filtered = {}
            pattern = filter_pattern.upper()
            for key, value in env_vars.items():
                if fnmatch.fnmatch(key.upper(), pattern):
                    filtered[key] = value
            return filtered
        
        return env_vars
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def execute_command(command: str, timeout: int = 30, capture_output: bool = True) -> Dict[str, Any]:
    """Execute a system command (use with caution)"""
    try:
        result = subprocess.run(
            command.split(),
            capture_output=capture_output,
            text=True,
            timeout=timeout
        )
        
        return {
            "command": command,
            "return_code": result.returncode,
            "stdout": result.stdout if capture_output else None,
            "stderr": result.stderr if capture_output else None,
            "success": result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {"error": f"Command timed out after {timeout} seconds"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_current_directory() -> str:
    """Get current working directory"""
    return os.getcwd()

@mcp.tool()
def get_user_home() -> str:
    """Get user home directory"""
    return str(Path.home())

# ========== Data Processing Tools ==========

@mcp.tool()
def process_csv(csv_data: str, operation: str = "info", column: str = None, delimiter: str = ",") -> Dict[str, Any]:
    """Process CSV data with various operations (info, stats, column, unique)"""
    try:
        # Read CSV data
        csv_file = io.StringIO(csv_data)
        reader = csv.DictReader(csv_file, delimiter=delimiter)
        rows = list(reader)
        
        if not rows:
            return {"error": "No data found in CSV"}
        
        headers = list(rows[0].keys())
        
        if operation == "info":
            return {
                "rows": len(rows),
                "columns": len(headers),
                "headers": headers,
                "sample_row": rows[0] if rows else None
            }
        
        elif operation == "stats" and column:
            if column not in headers:
                return {"error": f"Column '{column}' not found"}
            
            values = [row[column] for row in rows if row[column]]
            numeric_values = []
            
            # Try to convert to numbers
            for value in values:
                try:
                    numeric_values.append(float(value))
                except ValueError:
                    pass
            
            if numeric_values:
                return {
                    "column": column,
                    "total_values": len(values),
                    "numeric_values": len(numeric_values),
                    "min": min(numeric_values),
                    "max": max(numeric_values),
                    "mean": statistics.mean(numeric_values),
                    "median": statistics.median(numeric_values)
                }
            else:
                return {
                    "column": column,
                    "total_values": len(values),
                    "numeric_values": 0,
                    "note": "No numeric values found"
                }
        
        elif operation == "column" and column:
            if column not in headers:
                return {"error": f"Column '{column}' not found"}
            
            values = [row[column] for row in rows]
            return {
                "column": column,
                "values": values[:100]  # Limit to first 100 values
            }
        
        elif operation == "unique" and column:
            if column not in headers:
                return {"error": f"Column '{column}' not found"}
            
            values = [row[column] for row in rows if row[column]]
            unique_values = list(set(values))
            
            return {
                "column": column,
                "unique_count": len(unique_values),
                "unique_values": unique_values[:50]  # Limit to first 50 unique values
            }
        
        else:
            return {"error": "Invalid operation or missing column parameter"}
    
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def json_transform(json_data: str, operation: str, path: str = None) -> Any:
    """Transform JSON data (extract, keys, values, flatten)"""
    try:
        data = json.loads(json_data)
        
        if operation == "keys":
            if isinstance(data, dict):
                return list(data.keys())
            else:
                return {"error": "Data is not a JSON object"}
        
        elif operation == "values":
            if isinstance(data, dict):
                return list(data.values())
            else:
                return {"error": "Data is not a JSON object"}
        
        elif operation == "extract" and path:
            # Simple path extraction (e.g., "user.name" or "items[0].title")
            result = data
            parts = path.split('.')
            
            for part in parts:
                if '[' in part and ']' in part:
                    # Array access
                    key, index_part = part.split('[', 1)
                    index = int(index_part.rstrip(']'))
                    if key:
                        result = result[key]
                    result = result[index]
                else:
                    result = result[part]
            
            return result
        
        elif operation == "flatten":
            def flatten_dict(d, parent_key='', sep='.'):
                items = []
                for k, v in d.items():
                    new_key = f"{parent_key}{sep}{k}" if parent_key else k
                    if isinstance(v, dict):
                        items.extend(flatten_dict(v, new_key, sep=sep).items())
                    else:
                        items.append((new_key, v))
                return dict(items)
            
            if isinstance(data, dict):
                return flatten_dict(data)
            else:
                return {"error": "Data is not a JSON object"}
        
        else:
            return {"error": "Invalid operation"}
    
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON: {str(e)}"}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def calculate(expression: str) -> Dict[str, Any]:
    """Safely evaluate mathematical expressions"""
    try:
        # Only allow safe mathematical operations
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("_")
        }
        allowed_names.update({"abs": abs, "round": round, "min": min, "max": max})
        
        # Remove potentially dangerous functions
        dangerous = ['exec', 'eval', 'compile', 'open', 'input', '__import__']
        for name in dangerous:
            allowed_names.pop(name, None)
        
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        
        return {
            "expression": expression,
            "result": result,
            "type": type(result).__name__
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def statistics_summary(numbers: List[float]) -> Dict[str, float]:
    """Calculate statistical summary of a list of numbers"""
    try:
        if not numbers:
            return {"error": "Empty list provided"}
        
        return {
            "count": len(numbers),
            "sum": sum(numbers),
            "min": min(numbers),
            "max": max(numbers),
            "mean": statistics.mean(numbers),
            "median": statistics.median(numbers),
            "mode": statistics.mode(numbers) if len(set(numbers)) < len(numbers) else None,
            "std_dev": statistics.stdev(numbers) if len(numbers) > 1 else 0,
            "variance": statistics.variance(numbers) if len(numbers) > 1 else 0
        }
    except Exception as e:
        return {"error": str(e)}

# ========== Code Generation Tools ==========

@mcp.tool()
def generate_function(name: str, parameters: List[str], language: str = "python", description: str = "") -> str:
    """Generate a function template in specified language"""
    templates = {
        "python": '''def {name}({params}):
    """{description}"""
    # TODO: Implement function logic
    pass''',
        
        "javascript": '''function {name}({params}) {{
    // {description}
    // TODO: Implement function logic
}}''',
        
        "typescript": '''function {name}({params}): void {{
    // {description}
    // TODO: Implement function logic
}}''',
        
        "java": '''public void {name}({params}) {{
    // {description}
    // TODO: Implement method logic
}}''',
        
        "go": '''func {name}({params}) {{
    // {description}
    // TODO: Implement function logic
}}'''
    }
    
    if language.lower() not in templates:
        return f"Error: Unsupported language '{language}'"
    
    template = templates[language.lower()]
    params_str = ", ".join(parameters)
    
    return template.format(
        name=name,
        params=params_str,
        description=description or f"Function: {name}"
    )

@mcp.tool()
def generate_class(name: str, attributes: List[str], language: str = "python") -> str:
    """Generate a class template in specified language"""
    if language.lower() == "python":
        attrs_init = "\n        ".join([f"self.{attr} = {attr}" for attr in attributes])
        attrs_params = ", ".join(attributes)
        
        return f'''class {name}:
    """Class: {name}"""
    
    def __init__(self, {attrs_params}):
        {attrs_init}
    
    def __str__(self):
        return f"{name}({{', '.join([f'{attr}={{self.{attr}}}' for attr in attributes])}})"
'''
    
    elif language.lower() == "javascript":
        attrs_init = "\n        ".join([f"this.{attr} = {attr};" for attr in attributes])
        attrs_params = ", ".join(attributes)
        
        return f'''class {name} {{
    constructor({attrs_params}) {{
        {attrs_init}
    }}
    
    toString() {{
        return `{name}(${{", ".join([f"{attr}=${{this.{attr}}}" for attr in attributes])}})`;
    }}
}}'''
    
    else:
        return f"Error: Unsupported language '{language}'"

@mcp.tool()
def generate_api_client(base_url: str, endpoints: List[str], language: str = "python") -> str:
    """Generate API client code for specified endpoints"""
    if language.lower() == "python":
        methods = []
        for endpoint in endpoints:
            method_name = endpoint.lower().replace('/', '_').replace('-', '_')
            if method_name.startswith('_'):
                method_name = method_name[1:]
            
            methods.append(f'''    def {method_name}(self, **kwargs):
        """Call {endpoint} endpoint"""
        return self._request('GET', '{endpoint}', **kwargs)''')
        
        methods_str = "\n\n".join(methods)
        
        return f'''import requests

class APIClient:
    def __init__(self, base_url="{base_url}", api_key=None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        
        if api_key:
            self.session.headers.update({{
                'Authorization': f'Bearer {{api_key}}',
                'Content-Type': 'application/json'
            }})
    
    def _request(self, method, endpoint, **kwargs):
        url = f"{{self.base_url}}{{endpoint}}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

{methods_str}
'''
    else:
        return f"Error: Unsupported language '{language}'"

@mcp.tool()
def generate_dockerfile(base_image: str = "python:3.11-slim", port: int = 8000, requirements_file: str = "requirements.txt") -> str:
    """Generate a Dockerfile template"""
    return f'''FROM {base_image}

WORKDIR /app

COPY {requirements_file} .
RUN pip install --no-cache-dir -r {requirements_file}

COPY . .

EXPOSE {port}

CMD ["python", "app.py"]
'''

@mcp.tool()
def generate_makefile(project_name: str, language: str = "python") -> str:
    """Generate a Makefile template"""
    templates = {
        "python": f'''.PHONY: install test lint format clean run

install:
	pip install -r requirements.txt

test:
	pytest tests/

lint:
	flake8 {project_name}/
	black --check {project_name}/

format:
	black {project_name}/
	isort {project_name}/

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

run:
	python main.py
''',
        "node": f'''.PHONY: install test lint format clean run build

install:
	npm install

test:
	npm test

lint:
	npm run lint

format:
	npm run format

clean:
	rm -rf node_modules/
	rm -rf dist/

run:
	npm start

build:
	npm run build
'''
    }
    
    return templates.get(language.lower(), templates["python"])

@mcp.tool()
def generate_readme(project_name: str, description: str, language: str = "python") -> str:
    """Generate a README.md template"""
    install_cmd = {
        "python": "pip install -r requirements.txt",
        "node": "npm install",
        "go": "go mod tidy",
        "rust": "cargo build"
    }.get(language.lower(), "# Add installation instructions")
    
    run_cmd = {
        "python": "python main.py",
        "node": "npm start",
        "go": "go run main.go",
        "rust": "cargo run"
    }.get(language.lower(), "# Add run instructions")
    
    return f'''# {project_name}

{description}

## Installation

```bash
{install_cmd}
```

## Usage

```bash
{run_cmd}
```

## Features

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
'''

# ========== Validation Tools ==========

@mcp.tool()
def validate_email(email: str) -> bool:
    """Validate email address format"""
    if VALIDATORS_AVAILABLE:
        return validators.email(email) is True
    else:
        # Fallback regex validation
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

@mcp.tool()
def validate_url(url: str) -> bool:
    """Validate URL format"""
    if VALIDATORS_AVAILABLE:
        return validators.url(url) is True
    else:
        # Fallback regex validation
        pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b'
        return bool(re.match(pattern, url))

# ========== Markdown Tools ==========

@mcp.tool()
def markdown_to_html(markdown_text: str) -> str:
    """Convert Markdown to HTML"""
    if not MARKDOWN_AVAILABLE:
        return "Error: markdown library not installed"
    
    try:
        html = markdown.markdown(markdown_text, extensions=['extra', 'codehilite'])
        return html
    except Exception as e:
        return f"Error converting markdown: {str(e)}"

@mcp.tool()
def html_to_text(html_text: str) -> str:
    """Convert HTML to plain text"""
    if not BS4_AVAILABLE:
        return "Error: beautifulsoup4 not installed"
    
    try:
        soup = BeautifulSoup(html_text, 'html.parser')
        text = soup.get_text(separator='\n', strip=True)
        return text
    except Exception as e:
        return f"Error parsing HTML: {str(e)}"

# ========== Date/Time Tools ==========

@mcp.tool()
def parse_date(date_string: str, timezone: str = "UTC") -> Dict[str, Any]:
    """Parse date string to various formats"""
    if not DATEUTIL_AVAILABLE:
        return {"error": "python-dateutil not installed"}
    
    try:
        # Parse the date
        dt = date_parser.parse(date_string)
        
        # Apply timezone
        if timezone in pytz.all_timezones:
            tz = pytz.timezone(timezone)
            dt = tz.localize(dt) if dt.tzinfo is None else dt.astimezone(tz)
        
        return {
            "original": date_string,
            "iso_format": dt.isoformat(),
            "unix_timestamp": int(dt.timestamp()),
            "human_readable": dt.strftime("%B %d, %Y at %I:%M %p"),
            "date_only": dt.strftime("%Y-%m-%d"),
            "time_only": dt.strftime("%H:%M:%S"),
            "day_of_week": dt.strftime("%A"),
            "timezone": timezone
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def timezone_convert(time_string: str, from_tz: str, to_tz: str) -> Dict[str, str]:
    """Convert time between timezones"""
    if not DATEUTIL_AVAILABLE:
        return {"error": "python-dateutil not installed"}
    
    try:
        # Parse the time
        dt = date_parser.parse(time_string)
        
        # Apply source timezone
        if from_tz in pytz.all_timezones:
            from_timezone = pytz.timezone(from_tz)
            dt = from_timezone.localize(dt) if dt.tzinfo is None else dt
        
        # Convert to target timezone
        if to_tz in pytz.all_timezones:
            to_timezone = pytz.timezone(to_tz)
            dt_converted = dt.astimezone(to_timezone)
        else:
            return {"error": f"Invalid timezone: {to_tz}"}
        
        return {
            "original": time_string,
            "from_timezone": from_tz,
            "to_timezone": to_tz,
            "converted": dt_converted.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "iso_format": dt_converted.isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

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
        "version": "2.0.0",
        "available_tools": 62,
        "available_resources": 3,
        "available_prompts": 3,
        "categories": [
            "Text Processing",
            "File System",
            "YouTube Transcripts", 
            "Web Scraping",
            "Network/API",
            "System Information",
            "Data Processing",
            "Code Generation",
            "Date/Time",
            "Validation",
            "Markdown/HTML"
        ]
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