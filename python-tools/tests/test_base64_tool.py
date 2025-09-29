"""
Test Base64 Tool Plugin
"""

import sys
import unittest
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import registry
import plugins.base64_tool


class TestBase64Tool(unittest.TestCase):
    """Test Base64 tool functionality"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tool = registry.get_tool('base64')
    
    def test_tool_registration(self):
        """Test that tool is properly registered"""
        self.assertIn('base64', registry.list_tools())
        self.assertEqual(self.tool.config.name, 'base64')
        self.assertEqual(self.tool.config.category, 'encoding')
    
    def test_encode_basic(self):
        """Test basic encoding functionality"""
        input_data = {"text": "Hello World", "operation": "encode"}
        result = self.tool.run(input_data)
        
        self.assertNotIn('error', result)
        self.assertEqual(result['input'], 'Hello World')
        self.assertEqual(result['output'], 'SGVsbG8gV29ybGQ=')
        self.assertEqual(result['operation'], 'encode')
    
    def test_decode_basic(self):
        """Test basic decoding functionality"""
        input_data = {"text": "SGVsbG8gV29ybGQ=", "operation": "decode"}
        result = self.tool.run(input_data)
        
        self.assertNotIn('error', result)
        self.assertEqual(result['input'], 'SGVsbG8gV29ybGQ=')
        self.assertEqual(result['output'], 'Hello World')
        self.assertEqual(result['operation'], 'decode')
    
    def test_round_trip(self):
        """Test encoding and then decoding returns original"""
        original_text = "The quick brown fox jumps over the lazy dog"
        
        # Encode
        encode_input = {"text": original_text, "operation": "encode"}
        encoded_result = self.tool.run(encode_input)
        self.assertNotIn('error', encoded_result)
        
        # Decode
        decode_input = {"text": encoded_result['output'], "operation": "decode"}
        decoded_result = self.tool.run(decode_input)
        self.assertNotIn('error', decoded_result)
        
        self.assertEqual(decoded_result['output'], original_text)
    
    def test_empty_text_validation(self):
        """Test validation for empty text"""
        input_data = {"text": "", "operation": "encode"}
        result = self.tool.run(input_data)
        
        self.assertIn('error', result)
        self.assertIn('cannot be empty', result['error'])
    
    def test_whitespace_text_validation(self):
        """Test validation for whitespace-only text"""
        input_data = {"text": "   ", "operation": "encode"}
        result = self.tool.run(input_data)
        
        self.assertIn('error', result)
        self.assertIn('cannot be empty', result['error'])
    
    def test_invalid_base64_decode(self):
        """Test decoding invalid base64"""
        input_data = {"text": "invalid-base64!", "operation": "decode"}
        result = self.tool.run(input_data)
        
        self.assertIn('error', result)
        self.assertIn('failed', result['error'])
    
    def test_unicode_text(self):
        """Test with unicode characters"""
        unicode_text = "Hello 世界! 🌍"
        
        # Encode
        encode_input = {"text": unicode_text, "operation": "encode"}
        encoded_result = self.tool.run(encode_input)
        self.assertNotIn('error', encoded_result)
        
        # Decode
        decode_input = {"text": encoded_result['output'], "operation": "decode"}
        decoded_result = self.tool.run(decode_input)
        self.assertNotIn('error', decoded_result)
        
        self.assertEqual(decoded_result['output'], unicode_text)
    
    def test_input_schema(self):
        """Test input schema generation"""
        schema = self.tool.get_input_schema()
        self.assertIn('properties', schema)
        self.assertIn('text', schema['properties'])
        self.assertIn('operation', schema['properties'])
    
    def test_output_schema(self):
        """Test output schema generation"""
        schema = self.tool.get_output_schema()
        self.assertIn('properties', schema)
        self.assertIn('input', schema['properties'])
        self.assertIn('output', schema['properties'])
        self.assertIn('operation', schema['properties'])


if __name__ == '__main__':
    unittest.main(verbosity=2)