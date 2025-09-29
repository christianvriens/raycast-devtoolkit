#!/usr/bin/env python3
"""
Raycast DevToolkit Python Helpers
A collection of developer utilities that can be called from Raycast commands.
"""

from __future__ import annotations
import argparse
import json
import sys
import time
from typing import Any, Dict, List, Optional, Union


def output_json(data: Any, pretty: bool = True) -> None:
    """Output JSON to stdout for consumption by Raycast."""
    if pretty:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(data, ensure_ascii=False))


def output_error(message: str, code: int = 1) -> None:
    """Output error message to stderr and exit."""
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(code)


class DevTools:
    """Collection of developer utility functions."""
    
    @staticmethod
    def epoch_converter(epoch_input: str = None) -> Dict[str, Any]:
        """Convert epoch timestamp to human-readable formats."""
        from datetime import datetime, timezone
        
        if epoch_input is None:
            epoch = int(time.time())
        else:
            try:
                # Handle both seconds and milliseconds
                epoch_str = epoch_input.strip()
                if len(epoch_str) >= 13:  # milliseconds
                    epoch = int(epoch_str) // 1000
                else:  # seconds
                    epoch = int(epoch_str)
            except ValueError:
                raise ValueError(f"Invalid epoch timestamp: {epoch_input}")
        
        # Convert to datetime objects
        dt_utc = datetime.fromtimestamp(epoch, tz=timezone.utc)
        dt_local = dt_utc.astimezone()
        
        # Calculate relative time
        now = datetime.now(timezone.utc)
        diff = now - dt_utc
        
        return {
            "epoch": epoch,
            "utc": {
                "readable": dt_utc.strftime("%a, %d %b %Y %H:%M:%S %Z"),
                "iso": dt_utc.isoformat(),
                "ddmmyyyy": dt_utc.strftime("%d/%m/%Y %H:%M:%S")
            },
            "local": {
                "readable": dt_local.strftime("%a, %d %b %Y %H:%M:%S %Z"),
                "iso": dt_local.isoformat(),
                "ddmmyyyy": dt_local.strftime("%d/%m/%Y %H:%M:%S")
            },
            "relative": {
                "days": diff.days,
                "seconds": int(diff.total_seconds()),
                "human": DevTools._humanize_timedelta(diff)
            }
        }
    
    @staticmethod
    def jwt_decoder(token: str) -> Dict[str, Any]:
        """Decode JWT token without verification."""
        import base64
        import json
        from datetime import datetime
        
        try:
            # Split the token
            header_b64, payload_b64, signature_b64 = token.split('.')
            
            # Decode header and payload
            def decode_b64url(data: str) -> dict:
                # Add padding if needed
                padding = '=' * (-len(data) % 4)
                decoded = base64.urlsafe_b64decode(data + padding)
                return json.loads(decoded)
            
            header = decode_b64url(header_b64)
            payload = decode_b64url(payload_b64)
            
            # Extract common claims
            issued_at = payload.get('iat')
            expires_at = payload.get('exp')
            
            result = {
                "header": header,
                "payload": payload,
                "signature_length": len(base64.urlsafe_b64decode(signature_b64 + '=='))
            }
            
            # Add human-readable times
            if issued_at:
                result["issued_at_readable"] = datetime.fromtimestamp(issued_at).strftime("%Y-%m-%d %H:%M:%S UTC")
            if expires_at:
                result["expires_at_readable"] = datetime.fromtimestamp(expires_at).strftime("%Y-%m-%d %H:%M:%S UTC")
                now = time.time()
                result["is_expired"] = expires_at < now
                result["expires_in_seconds"] = max(0, expires_at - now)
            
            return result
            
        except Exception as e:
            raise ValueError(f"Invalid JWT token: {str(e)}")
    
    @staticmethod
    def url_encoder(text: str, decode: bool = False) -> Dict[str, str]:
        """URL encode or decode text."""
        from urllib.parse import quote, unquote
        
        if decode:
            return {
                "input": text,
                "output": unquote(text),
                "operation": "decode"
            }
        else:
            return {
                "input": text,
                "output": quote(text),
                "operation": "encode"
            }
    
    @staticmethod
    def base64_converter(text: str, decode: bool = False) -> Dict[str, str]:
        """Base64 encode or decode text."""
        import base64
        
        try:
            if decode:
                decoded = base64.b64decode(text).decode('utf-8')
                return {
                    "input": text,
                    "output": decoded,
                    "operation": "decode"
                }
            else:
                encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
                return {
                    "input": text,
                    "output": encoded,
                    "operation": "encode"
                }
        except Exception as e:
            raise ValueError(f"Base64 operation failed: {str(e)}")
    
    @staticmethod
    def hash_generator(text: str, algorithm: str = "sha256") -> Dict[str, str]:
        """Generate hash of text using specified algorithm."""
        import hashlib
        
        algorithms = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512
        }
        
        if algorithm not in algorithms:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        hash_func = algorithms[algorithm]()
        hash_func.update(text.encode('utf-8'))
        
        return {
            "input": text,
            "algorithm": algorithm,
            "hash": hash_func.hexdigest()
        }
    
    @staticmethod
    def json_formatter(text: str, minify: bool = False) -> Dict[str, Any]:
        """Format JSON text (pretty print or minify)."""
        try:
            parsed = json.loads(text)
            if minify:
                formatted = json.dumps(parsed, separators=(',', ':'))
            else:
                formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
            
            return {
                "input": text,
                "output": formatted,
                "operation": "minify" if minify else "format",
                "valid": True
            }
        except json.JSONDecodeError as e:
            return {
                "input": text,
                "error": str(e),
                "valid": False
            }
    
    @staticmethod
    def uuid_generator(version: int = 4, count: int = 1) -> Dict[str, Any]:
        """Generate UUID(s)."""
        import uuid
        
        generators = {
            1: uuid.uuid1,
            4: uuid.uuid4
        }
        
        if version not in generators:
            raise ValueError(f"Unsupported UUID version: {version}")
        
        uuids = [str(generators[version]()) for _ in range(count)]
        
        return {
            "version": version,
            "count": count,
            "uuids": uuids
        }
    
    @staticmethod
    def color_converter(color: str, output_format: str = "all") -> Dict[str, Any]:
        """Convert color between different formats."""
        def hex_to_rgb(hex_color: str) -> tuple:
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        def rgb_to_hex(r: int, g: int, b: int) -> str:
            return f"#{r:02x}{g:02x}{b:02x}"
        
        def rgb_to_hsl(r: int, g: int, b: int) -> tuple:
            r, g, b = r/255.0, g/255.0, b/255.0
            max_val = max(r, g, b)
            min_val = min(r, g, b)
            diff = max_val - min_val
            
            # Lightness
            l = (max_val + min_val) / 2
            
            if diff == 0:
                h = s = 0
            else:
                # Saturation
                s = diff / (2 - max_val - min_val) if l > 0.5 else diff / (max_val + min_val)
                
                # Hue
                if max_val == r:
                    h = ((g - b) / diff + (6 if g < b else 0)) / 6
                elif max_val == g:
                    h = ((b - r) / diff + 2) / 6
                else:
                    h = ((r - g) / diff + 4) / 6
            
            return int(h * 360), int(s * 100), int(l * 100)
        
        try:
            # Determine input format and convert
            if color.startswith('#'):
                # HEX input
                r, g, b = hex_to_rgb(color)
                h, s, l = rgb_to_hsl(r, g, b)
            elif color.startswith('rgb'):
                # RGB input
                import re
                match = re.search(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color)
                if match:
                    r, g, b = map(int, match.groups())
                    h, s, l = rgb_to_hsl(r, g, b)
                else:
                    raise ValueError("Invalid RGB format")
            else:
                raise ValueError("Unsupported color format")
            
            return {
                "input": color,
                "hex": rgb_to_hex(r, g, b),
                "rgb": f"rgb({r}, {g}, {b})",
                "hsl": f"hsl({h}, {s}%, {l}%)",
                "values": {
                    "r": r, "g": g, "b": b,
                    "h": h, "s": s, "l": l
                }
            }
        except Exception as e:
            raise ValueError(f"Color conversion failed: {str(e)}")
    
    @staticmethod
    def _humanize_timedelta(delta) -> str:
        """Convert timedelta to human readable string."""
        seconds = int(delta.total_seconds())
        
        if seconds < 0:
            return f"{abs(seconds)} seconds in the future"
        
        if seconds < 60:
            return f"{seconds} seconds ago"
        elif seconds < 3600:
            return f"{seconds // 60} minutes ago"
        elif seconds < 86400:
            return f"{seconds // 3600} hours ago"
        else:
            return f"{seconds // 86400} days ago"


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="DevToolkit Python Helpers")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Epoch converter
    epoch_parser = subparsers.add_parser('epoch', help='Convert epoch timestamp')
    epoch_parser.add_argument('timestamp', nargs='?', help='Epoch timestamp (empty for current time)')
    
    # JWT decoder
    jwt_parser = subparsers.add_parser('jwt', help='Decode JWT token')
    jwt_parser.add_argument('token', help='JWT token to decode')
    
    # URL encoder/decoder
    url_parser = subparsers.add_parser('url', help='URL encode/decode')
    url_parser.add_argument('text', help='Text to encode/decode')
    url_parser.add_argument('--decode', action='store_true', help='Decode instead of encode')
    
    # Base64 encoder/decoder
    b64_parser = subparsers.add_parser('base64', help='Base64 encode/decode')
    b64_parser.add_argument('text', help='Text to encode/decode')
    b64_parser.add_argument('--decode', action='store_true', help='Decode instead of encode')
    
    # Hash generator
    hash_parser = subparsers.add_parser('hash', help='Generate hash')
    hash_parser.add_argument('text', help='Text to hash')
    hash_parser.add_argument('--algorithm', choices=['md5', 'sha1', 'sha256', 'sha512'], default='sha256', help='Hash algorithm')
    
    # JSON formatter
    json_parser = subparsers.add_parser('json', help='Format JSON')
    json_parser.add_argument('text', help='JSON text to format')
    json_parser.add_argument('--minify', action='store_true', help='Minify instead of format')
    
    # UUID generator
    uuid_parser = subparsers.add_parser('uuid', help='Generate UUID')
    uuid_parser.add_argument('--version', type=int, choices=[1, 4], default=4, help='UUID version')
    uuid_parser.add_argument('--count', type=int, default=1, help='Number of UUIDs to generate')
    
    # Color converter
    color_parser = subparsers.add_parser('color', help='Convert color formats')
    color_parser.add_argument('color', help='Color to convert (hex or rgb format)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'epoch':
            result = DevTools.epoch_converter(args.timestamp)
        elif args.command == 'jwt':
            result = DevTools.jwt_decoder(args.token)
        elif args.command == 'url':
            result = DevTools.url_encoder(args.text, args.decode)
        elif args.command == 'base64':
            result = DevTools.base64_converter(args.text, args.decode)
        elif args.command == 'hash':
            result = DevTools.hash_generator(args.text, args.algorithm)
        elif args.command == 'json':
            result = DevTools.json_formatter(args.text, args.minify)
        elif args.command == 'uuid':
            result = DevTools.uuid_generator(args.version, args.count)
        elif args.command == 'color':
            result = DevTools.color_converter(args.color)
        
        output_json(result)
        return 0
    
    except Exception as e:
        output_error(str(e))


if __name__ == '__main__':
    sys.exit(main())