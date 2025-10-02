#!/usr/bin/env python3
"""
Test URL Tool Plugin
Tests the URL encoding/decoding functionality
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins.url_tool import UrlTool, UrlInput


class TestUrlTool(unittest.TestCase):
    """Test cases for URL tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tool = UrlTool()
    
    def test_tool_config(self):
        """Test tool configuration"""
        config = self.tool.get_config()
        self.assertEqual(config.name, "url")
        self.assertEqual(config.category, "encoding")
        self.assertIn("url", config.keywords)
    
    def test_url_encoding(self):
        """Test URL encoding"""
        input_data = UrlInput(text="Hello World!", operation="encode")
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.output, "Hello%20World%21")
        self.assertEqual(result.operation, "encode")
    
    def test_url_decoding(self):
        """Test URL decoding"""
        input_data = UrlInput(text="Hello%20World%21", operation="decode")
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.output, "Hello World!")
        self.assertEqual(result.operation, "decode")
    
    def test_url_encoding_special_chars(self):
        """Test URL encoding with special characters"""
        special_text = "user@example.com/path?query=value&other=123"
        input_data = UrlInput(text=special_text, operation="encode")
        result = self.tool.execute(input_data)
        
        self.assertIn("user%40example.com", result.output)
        self.assertIn("%3F", result.output)  # ?
        self.assertIn("%3D", result.output)  # =
        self.assertIn("%26", result.output)  # &
    
    def test_url_roundtrip(self):
        """Test encoding then decoding returns original"""
        original_text = "Hello World! @#$%^&*()"
        
        # Encode
        encode_input = UrlInput(text=original_text, operation="encode")
        encode_result = self.tool.execute(encode_input)
        
        # Decode
        decode_input = UrlInput(text=encode_result.output, operation="decode")
        decode_result = self.tool.execute(decode_input)
        
        self.assertEqual(decode_result.output, original_text)
    
    def test_empty_text(self):
        """Test handling empty text"""
        with self.assertRaises(Exception):
            UrlInput(text="", operation="encode")
    
    def test_invalid_operation(self):
        """Test handling invalid operation"""
        with self.assertRaises(Exception):
            UrlInput(text="test", operation="invalid")  # type: ignore[arg-type]
    
    def test_unicode_handling(self):
        """Test Unicode character handling"""
        unicode_text = "Hello 世界! 🌍"
        input_data = UrlInput(text=unicode_text, operation="encode")
        result = self.tool.execute(input_data)
        
        # Should encode Unicode characters
        self.assertNotEqual(result.output, unicode_text)
        self.assertIn("%", result.output)
        
        # Decode back
        decode_input = UrlInput(text=result.output, operation="decode")
        decode_result = self.tool.execute(decode_input)
        self.assertEqual(decode_result.output, unicode_text)
    
    def test_get_schemas(self):
        """Test schema generation"""
        input_schema = self.tool.get_input_schema()
        output_schema = self.tool.get_output_schema()
        
        self.assertIn("properties", input_schema)
        self.assertIn("text", input_schema["properties"])
        self.assertIn("operation", input_schema["properties"])
        
        self.assertIn("properties", output_schema)
        self.assertIn("output", output_schema["properties"])


if __name__ == "__main__":
    unittest.main()