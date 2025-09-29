#!/usr/bin/env python3
"""
Test Hash Tool Plugin
Tests the hash generation functionality
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins.hash_tool import HashTool, HashInput


class TestHashTool(unittest.TestCase):
    """Test cases for Hash tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tool = HashTool()
    
    def test_tool_config(self):
        """Test tool configuration"""
        config = self.tool.get_config()
        self.assertEqual(config.name, "hash")
        self.assertEqual(config.category, "security")
        self.assertIn("hash", config.keywords)
    
    def test_md5_hash(self):
        """Test MD5 hash generation"""
        input_data = HashInput(text="hello", algorithm="md5")
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.hash, "5d41402abc4b2a76b9719d911017c592")
        self.assertEqual(result.algorithm, "md5")
        self.assertEqual(result.length, 32)
    
    def test_sha1_hash(self):
        """Test SHA1 hash generation"""
        input_data = HashInput(text="hello", algorithm="sha1")
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.hash, "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d")
        self.assertEqual(result.algorithm, "sha1")
        self.assertEqual(result.length, 40)
    
    def test_sha256_hash(self):
        """Test SHA256 hash generation"""
        input_data = HashInput(text="hello", algorithm="sha256")
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.hash, "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824")
        self.assertEqual(result.algorithm, "sha256")
        self.assertEqual(result.length, 64)
    
    def test_sha512_hash(self):
        """Test SHA512 hash generation"""
        input_data = HashInput(text="hello", algorithm="sha512")
        result = self.tool.execute(input_data)
        
        expected = "9b71d224bd62f3785d96d46ad3ea3d73319bfbc2890caadae2dff72519673ca72323c3d99ba5c11d7c7acc6e14b8c5da0c4663475c2e5c3adef46f73bcdec043"
        self.assertEqual(result.hash, expected)
        self.assertEqual(result.algorithm, "sha512")
        self.assertEqual(result.length, 128)
    
    def test_empty_text(self):
        """Test handling empty text"""
        with self.assertRaises(Exception):
            HashInput(text="", algorithm="sha256")
    
    def test_invalid_algorithm(self):
        """Test handling invalid algorithm"""
        with self.assertRaises(Exception):
            HashInput(text="test", algorithm="invalid")
    
    def test_unicode_text(self):
        """Test hashing Unicode text"""
        input_data = HashInput(text="Hello 世界! 🌍", algorithm="sha256")
        result = self.tool.execute(input_data)
        
        self.assertEqual(len(result.hash), 64)  # SHA256 is always 64 chars
        self.assertEqual(result.algorithm, "sha256")
    
    def test_large_text(self):
        """Test hashing large text"""
        large_text = "A" * 10000  # 10k characters
        input_data = HashInput(text=large_text, algorithm="sha256")
        result = self.tool.execute(input_data)
        
        self.assertEqual(len(result.hash), 64)
        self.assertEqual(result.length, 64)
    
    def test_consistency(self):
        """Test that same input produces same hash"""
        text = "consistency test"
        
        input1 = HashInput(text=text, algorithm="sha256")
        result1 = self.tool.execute(input1)
        
        input2 = HashInput(text=text, algorithm="sha256")
        result2 = self.tool.execute(input2)
        
        self.assertEqual(result1.hash, result2.hash)
    
    def test_get_schemas(self):
        """Test schema generation"""
        input_schema = self.tool.get_input_schema()
        output_schema = self.tool.get_output_schema()
        
        self.assertIn("properties", input_schema)
        self.assertIn("text", input_schema["properties"])
        self.assertIn("algorithm", input_schema["properties"])
        
        self.assertIn("properties", output_schema)
        self.assertIn("hash", output_schema["properties"])


if __name__ == "__main__":
    unittest.main()