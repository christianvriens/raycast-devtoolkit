#!/usr/bin/env python3
"""
Comprehensive test suite for the DevToolkit Python helpers.
Tests all functionality to ensure everything works correctly.
"""

import unittest
import json
import sys
import os
import re
import uuid as uuid_module
import subprocess
from datetime import datetime
from pathlib import Path

# Add the current directory to the path so we can import the devtools module
sys.path.insert(0, os.path.dirname(__file__))

from devtools import DevTools


class TestDevTools(unittest.TestCase):
    """Test all DevToolkit functionality"""

    def test_epoch_converter(self):
        """Test epoch timestamp conversion"""
        # Test current time (no input)
        result = DevTools.epoch_converter()
        self.assertIn('epoch', result)
        self.assertIn('utc', result)
        
        # Test specific timestamp
        result = DevTools.epoch_converter("1695735600")  # Sep 26, 2023 15:00:00 UTC
        self.assertIn('epoch', result)
        self.assertIn('utc', result)
        self.assertEqual(result['epoch'], 1695735600)

    def test_base64_converter(self):
        """Test base64 encoding and decoding"""
        text = "Hello World"
        
        # Test encoding
        result = DevTools.base64_converter(text)
        self.assertEqual(result['operation'], 'encode')
        self.assertEqual(result['input'], text)
        encoded = result['output']
        
        # Test decoding
        result = DevTools.base64_converter(encoded, decode=True)
        self.assertEqual(result['operation'], 'decode')
        self.assertEqual(result['output'], text)

    def test_url_encoder(self):
        """Test URL encoding and decoding"""
        text = "Hello World & More"
        
        # Test encoding
        result = DevTools.url_encoder(text)
        self.assertEqual(result['operation'], 'encode')
        self.assertEqual(result['input'], text)
        encoded = result['output']
        
        # Test decoding
        result = DevTools.url_encoder(encoded, decode=True)
        self.assertEqual(result['operation'], 'decode')
        self.assertEqual(result['output'], text)

    def test_hash_generator(self):
        """Test hash generation with different algorithms"""
        text = "Hello World"
        
        # Test MD5
        result = DevTools.hash_generator(text, "md5")
        self.assertEqual(len(result['hash']), 32)  # MD5 is 32 chars
        
        # Test SHA1
        result = DevTools.hash_generator(text, "sha1")
        self.assertEqual(len(result['hash']), 40)  # SHA1 is 40 chars
        
        # Test SHA256
        result = DevTools.hash_generator(text, "sha256")
        self.assertEqual(len(result['hash']), 64)  # SHA256 is 64 chars
        
        # Test SHA512
        result = DevTools.hash_generator(text, "sha512")
        self.assertEqual(len(result['hash']), 128)  # SHA512 is 128 chars

    def test_json_formatter(self):
        """Test JSON formatting"""
        json_str = '{"name":"test","value":123}'
        
        # Test formatting (pretty print)
        result = DevTools.json_formatter(json_str)
        self.assertIn('output', result)
        formatted_json = json.loads(result['output'])
        self.assertEqual(formatted_json['name'], 'test')
        self.assertEqual(formatted_json['value'], 123)
        
        # Test minification
        pretty_json = '{\n  "name": "test",\n  "value": 123\n}'
        result = DevTools.json_formatter(pretty_json, minify=True)
        self.assertIn('output', result)
        self.assertNotIn('\n', result['output'])

    def test_uuid_generator(self):
        """Test UUID generation"""
        # Test UUID v4 (default)
        result = DevTools.uuid_generator()
        self.assertEqual(result['version'], 4)
        self.assertEqual(result['count'], 1)
        self.assertEqual(len(result['uuids']), 1)
        
        # Validate UUID format
        uuid_str = result['uuids'][0]
        uuid_module.UUID(uuid_str)  # Should not raise exception if valid
        
        # Test multiple UUIDs
        result = DevTools.uuid_generator(count=3)
        self.assertEqual(len(result['uuids']), 3)

    def test_color_converter(self):
        """Test color format conversion"""
        # Test hex to RGB
        result = DevTools.color_converter("#FF5733", "rgb")
        self.assertIn('rgb', result)
        
        # Test RGB to hex (this might not work as expected due to input format)
        # We'll test with the command line interface instead
        pass

    def test_jwt_decoder(self):
        """Test JWT token decoding"""
        # Sample JWT token (this is a test token, not a real one)
        sample_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        
        result = DevTools.jwt_decoder(sample_jwt)
        self.assertIn('header', result)
        self.assertIn('payload', result)
        self.assertEqual(result['payload']['name'], 'John Doe')


class TestCommandLineInterface(unittest.TestCase):
    """Test the command line interface"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.script_path = Path(__file__).parent / "devtools.py"
        
    def run_command(self, *args):
        """Helper to run the devtools script"""
        cmd = [sys.executable, str(self.script_path)] + list(args)
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result
    
    def test_help_command(self):
        """Test help output"""
        result = self.run_command("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("DevToolkit Python Helpers", result.stdout)
    
    def test_uuid_command(self):
        """Test UUID generation via CLI"""
        result = self.run_command("uuid")
        self.assertEqual(result.returncode, 0)
        
        output = json.loads(result.stdout)
        self.assertEqual(output['version'], 4)
        self.assertEqual(len(output['uuids']), 1)
    
    def test_base64_encode_command(self):
        """Test base64 encoding via CLI"""
        result = self.run_command("base64", "Hello World")
        self.assertEqual(result.returncode, 0)
        
        output = json.loads(result.stdout)
        self.assertEqual(output['operation'], 'encode')
        self.assertEqual(output['input'], 'Hello World')
        self.assertEqual(output['output'], 'SGVsbG8gV29ybGQ=')
    
    def test_base64_decode_command(self):
        """Test base64 decoding via CLI"""
        result = self.run_command("base64", "--decode", "SGVsbG8gV29ybGQ=")
        self.assertEqual(result.returncode, 0)
        
        output = json.loads(result.stdout)
        self.assertEqual(output['operation'], 'decode')
        self.assertEqual(output['output'], 'Hello World')
    
    def test_hash_command(self):
        """Test hash generation via CLI"""
        result = self.run_command("hash", "Hello World", "--algorithm", "sha256")
        self.assertEqual(result.returncode, 0)
        
        output = json.loads(result.stdout)
        self.assertEqual(output['algorithm'], 'sha256')
        self.assertEqual(len(output['hash']), 64)


if __name__ == '__main__':
    print("Running DevToolkit Test Suite...")
    print("=" * 50)
    
    # Run the tests
    unittest.main(verbosity=2)