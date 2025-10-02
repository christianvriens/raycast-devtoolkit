#!/usr/bin/env python3
"""
DevToolkit - Plugin-Based Developer Utilities
A modular collection of developer tools with Pydantic validation
"""

import sys
import json
import argparse
from typing import Any, Dict, List
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import core components
from core import registry
# Import all plugins (triggers registration)
import plugins

def output_json(data: Any, pretty: bool = True) -> None:
    """Output JSON to stdout"""
    if pretty:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(data, ensure_ascii=False))

def output_error(message: str, code: int = 1) -> None:
    """Output error message to stderr and exit"""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(code)

def list_tools_command() -> Dict[str, Any]:
    """List all available tools"""
    tools = registry.list_tools()
    categories = registry.get_all_categories()
    
    tools_by_category = {}
    for category in categories:
        tools_by_category[category] = registry.get_tools_by_category(category)
    
    return {
        "total_tools": len(tools),
        "categories": categories,
        "tools": tools,
        "tools_by_category": tools_by_category
    }

def tool_info_command(tool_name: str) -> Dict[str, Any]:
    """Get detailed information about a specific tool"""
    try:
        return registry.get_tool_info(tool_name)
    except ValueError as e:
        raise ValueError(f"Tool '{tool_name}' not found. Available tools: {', '.join(registry.list_tools())}")

def execute_tool_command(tool_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Execute a tool with given input data"""
    try:
        tool = registry.get_tool(tool_name)
        return tool.run(input_data)
    except ValueError as e:
        raise ValueError(f"Tool '{tool_name}' not found. Available tools: {', '.join(registry.list_tools())}")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="DevToolkit - Plugin-based developer utilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                           # List all tools
  %(prog)s info base64                    # Get tool information
  %(prog)s run base64 '{"text":"hello"}'  # Execute tool
  %(prog)s base64 hello                   # Quick execution (legacy)
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List tools command
    list_parser = subparsers.add_parser('list', help='List all available tools')
    
    # Tool info command
    info_parser = subparsers.add_parser('info', help='Get information about a tool')
    info_parser.add_argument('tool', help='Tool name')
    
    # Run tool command
    run_parser = subparsers.add_parser('run', help='Execute a tool')
    run_parser.add_argument('tool', help='Tool name')
    run_parser.add_argument('input', help='Input data as JSON string')
    
    # Legacy commands
    legacy_parser = subparsers.add_parser('base64', help='Base64 encode/decode (legacy)')
    legacy_parser.add_argument('text', help='Text to encode/decode')
    legacy_parser.add_argument('--decode', action='store_true', help='Decode instead of encode')
    
    # URL
    url_parser = subparsers.add_parser('url', help='URL encode/decode (legacy)')
    url_parser.add_argument('text', help='Text to encode/decode')
    url_parser.add_argument('--decode', action='store_true', help='Decode instead of encode')
    
    # Hash
    hash_parser = subparsers.add_parser('hash', help='Generate hash (legacy)')
    hash_parser.add_argument('text', help='Text to hash')
    hash_parser.add_argument('--algorithm', choices=['md5', 'sha1', 'sha256', 'sha512'], 
                           default='sha256', help='Hash algorithm')
    
    # JWT
    jwt_parser = subparsers.add_parser('jwt', help='Decode JWT token (legacy)')
    jwt_parser.add_argument('token', help='JWT token to decode')
    
    # JSON
    json_parser = subparsers.add_parser('json', help='Format JSON (legacy)')
    json_parser.add_argument('text', help='JSON text to format')
    json_parser.add_argument('--minify', action='store_true', help='Minify instead of format')
    
    # UUID
    uuid_parser = subparsers.add_parser('uuid', help='Generate UUID (legacy)')
    uuid_parser.add_argument('--version', type=int, choices=[1, 4], default=4, help='UUID version')
    uuid_parser.add_argument('--count', type=int, default=1, help='Number of UUIDs to generate')
    
    # Epoch
    epoch_parser = subparsers.add_parser('epoch', help='Convert epoch timestamp (legacy)')
    epoch_parser.add_argument('timestamp', nargs='?', help='Epoch timestamp (leave empty for current time)')
    
    # Color
    color_parser = subparsers.add_parser('color', help='Convert color formats (legacy)')
    color_parser.add_argument('color', help='Color value to convert')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'list':
            result = list_tools_command()
        elif args.command == 'info':
            result = tool_info_command(args.tool)
        elif args.command == 'run':
            try:
                input_data = json.loads(args.input)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON input: {e}")
            result = execute_tool_command(args.tool, input_data)
        
        # Legacy command support
        elif args.command == 'base64':
            input_data = {
                "text": args.text,
                "operation": "decode" if args.decode else "encode"
            }
            result = execute_tool_command('base64', input_data)
        elif args.command == 'url':
            input_data = {
                "text": args.text,
                "operation": "decode" if args.decode else "encode"
            }
            result = execute_tool_command('url', input_data)
        elif args.command == 'hash':
            input_data = {
                "text": args.text,
                "algorithm": args.algorithm
            }
            result = execute_tool_command('hash', input_data)
        elif args.command == 'jwt':
            input_data = {
                "token": args.token
            }
            result = execute_tool_command('jwt', input_data)
        elif args.command == 'json':
            # If caller passes '-' as the text argument, read the JSON payload from stdin.
            text_value = args.text
            if text_value == '-':
                try:
                    text_value = sys.stdin.read()
                except Exception:
                    raise ValueError("Failed to read JSON from stdin")

            input_data = {
                "text": text_value,
                "minify": args.minify
            }
            result = execute_tool_command('json', input_data)
        elif args.command == 'uuid':
            input_data = {
                "version": args.version,
                "count": args.count
            }
            result = execute_tool_command('uuid', input_data)
        elif args.command == 'epoch':
            input_data = {
                "timestamp": args.timestamp
            }
            result = execute_tool_command('epoch', input_data)
        elif args.command == 'color':
            input_data = {
                "color": args.color
            }
            result = execute_tool_command('color', input_data)
        else:
            parser.print_help()
            return 1
        
        output_json(result)
        return 0
    
    except Exception as e:
        output_error(str(e))

if __name__ == '__main__':
    sys.exit(main())