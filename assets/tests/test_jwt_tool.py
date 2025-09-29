#!/usr/bin/env python3
"""
Test JWT Tool Plugin
Tests the JWT decoding functionality
"""

import unittest
import sys
import os
from datetime import datetime, timezone

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins.jwt_tool import JWTTool, JWTInput


class TestJWTTool(unittest.TestCase):
    """Test cases for JWT tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tool = JWTTool()
        
        # Sample JWT token for testing (no signature verification, just decoding)
        # Header: {"alg": "HS256", "typ": "JWT"}
        # Payload: {"sub": "1234567890", "name": "John Doe", "iat": 1516239022}
        self.sample_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    
    def test_tool_config(self):
        """Test tool configuration"""
        config = self.tool.get_config()
        self.assertEqual(config.name, "jwt")
        self.assertEqual(config.category, "security")
        self.assertIn("jwt", config.keywords)
    
    def test_valid_jwt_decoding(self):
        """Test decoding a valid JWT token"""
        input_data = JWTInput(token=self.sample_jwt)
        result = self.tool.execute(input_data)
        
        self.assertTrue(result.valid_format)
        self.assertEqual(result.header["alg"], "HS256")
        self.assertEqual(result.header["typ"], "JWT")
        self.assertEqual(result.payload["sub"], "1234567890")
        self.assertEqual(result.payload["name"], "John Doe")
        self.assertEqual(result.payload["iat"], 1516239022)
    
    def test_invalid_jwt_format(self):
        """Test handling invalid JWT format"""
        input_data = JWTInput(token="invalid.jwt")
        result = self.tool.execute(input_data)
        
        self.assertFalse(result.valid_format)
        self.assertEqual(result.header, {})
        self.assertEqual(result.payload, {})
    
    def test_empty_token(self):
        """Test handling empty token"""
        with self.assertRaises(Exception):
            JWTInput(token="")
    
    def test_malformed_base64(self):
        """Test handling malformed base64 in JWT"""
        malformed_jwt = "invalid_base64.another_invalid.signature"
        input_data = JWTInput(token=malformed_jwt)
        
        with self.assertRaises(ValueError):
            self.tool.execute(input_data)
    
    def test_jwt_with_exp_claim(self):
        """Test JWT with expiration claim"""
        # Create a JWT with exp claim (expired)
        # Header: {"alg": "HS256", "typ": "JWT"}
        # Payload: {"sub": "1234567890", "exp": 1516239022, "iat": 1516239022}
        jwt_with_exp = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZXhwIjoxNTE2MjM5MDIyLCJpYXQiOjE1MTYyMzkwMjJ9.4Adcj3UFYzPUVaVF43FmMab6RlaQD8A9V8wFzzht-KQ"
        
        input_data = JWTInput(token=jwt_with_exp)
        result = self.tool.execute(input_data)
        
        self.assertTrue(result.valid_format)
        self.assertIsNotNone(result.expires_at)
        self.assertIsNotNone(result.expires_at_readable)
        self.assertIsNotNone(result.is_expired)
        # Token from 2018 should be expired
        self.assertTrue(result.is_expired)
    
    def test_input_validation(self):
        """Test input validation"""
        # Valid input
        valid_input = JWTInput(token=self.sample_jwt)
        self.assertEqual(valid_input.token, self.sample_jwt)
        
        # Input with whitespace should be stripped
        input_with_spaces = JWTInput(token="  " + self.sample_jwt + "  ")
        self.assertEqual(input_with_spaces.token, self.sample_jwt)
    
    def test_get_schemas(self):
        """Test schema generation"""
        input_schema = self.tool.get_input_schema()
        output_schema = self.tool.get_output_schema()
        
        self.assertIn("properties", input_schema)
        self.assertIn("token", input_schema["properties"])
        
        self.assertIn("properties", output_schema)
        self.assertIn("header", output_schema["properties"])
        self.assertIn("payload", output_schema["properties"])


if __name__ == "__main__":
    unittest.main()