#!/usr/bin/env python3
"""
Test JSON Tool Plugin
Tests the JSON formatting and validation functionality
"""

import unittest
import sys
import os
import json

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins.json_tool import JSONTool, JSONInput


class TestJSONTool(unittest.TestCase):
    """Test cases for JSON tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tool = JSONTool()
        self.sample_json = '{"name":"John","age":30,"city":"New York"}'
        self.sample_formatted = '''{
  "age": 30,
  "city": "New York",
  "name": "John"
}'''
    
    def test_tool_config(self):
        """Test tool configuration"""
        config = self.tool.get_config()
        self.assertEqual(config.name, "json")
        self.assertEqual(config.category, "text")
        self.assertIn("json", config.keywords)
    
    def test_json_formatting(self):
        """Test JSON formatting"""
        input_data = JSONInput(text=self.sample_json, minify=False)
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.operation, "format")
        self.assertTrue(result.valid)
        self.assertIn("age", result.formatted)
        self.assertTrue(len(result.formatted) > len(self.sample_json))  # Formatted is longer
        
        # Should be valid JSON
        parsed = json.loads(result.formatted)
        self.assertEqual(parsed["name"], "John")
    
    def test_json_minifying(self):
        """Test JSON minifying"""
        formatted_json = '''{
  "name": "John",
  "age": 30,
  "city": "New York"
}'''
        input_data = JSONInput(text=formatted_json, minify=True)
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.operation, "minify")
        self.assertTrue(result.valid)
        self.assertTrue(len(result.formatted) < len(formatted_json))  # Minified is shorter
        self.assertNotIn("\n", result.formatted)  # No newlines in minified
        self.assertNotIn("  ", result.formatted)  # No double spaces

    def test_json_minify_with_html_value(self):
        """Ensure JSON minify works when a value contains HTML with quotes and braces"""
        complex_value = (
            'U searched for <span class="sqr-underline sqr-italic">{{old}}</span>, '
            "but we didn't find any results. U searched for "
            '<span class="sqr-underline sqr-italic">{{new}}</span>, we found {{count}} result.'
        )
        # Build a JSON object containing that string as a value
        obj = {"spellcheck_results_one": complex_value}
        input_text = json.dumps(obj, ensure_ascii=False)

        input_data = JSONInput(text=input_text, minify=True)
        result = self.tool.execute(input_data)

        self.assertEqual(result.operation, "minify")
        self.assertTrue(result.valid)
        # minified result should parse back to the same structure
        parsed = json.loads(result.formatted)
        self.assertIn("spellcheck_results_one", parsed)
        self.assertEqual(parsed["spellcheck_results_one"], complex_value)
    
    def test_invalid_json(self):
        """Test handling invalid JSON"""
        invalid_json = '{"name":"John","age":30,}'  # Trailing comma
        input_data = JSONInput(text=invalid_json)
        
        with self.assertRaises(ValueError):
            self.tool.execute(input_data)
    
    def test_complex_json(self):
        """Test formatting complex JSON"""
        complex_json = '{"users":[{"name":"John","details":{"age":30,"skills":["python","javascript"]}}],"meta":{"version":"1.0"}}'
        input_data = JSONInput(text=complex_json, minify=False)
        result = self.tool.execute(input_data)
        
        self.assertTrue(result.valid)
        self.assertIn("users", result.formatted)
        self.assertIn("skills", result.formatted)
        
        # Should maintain structure
        parsed = json.loads(result.formatted)
        self.assertEqual(len(parsed["users"]), 1)
        self.assertEqual(len(parsed["users"][0]["details"]["skills"]), 2)
    
    def test_empty_json(self):
        """Test handling empty JSON"""
        with self.assertRaises(Exception):
            JSONInput(text="")
    
    def test_size_calculation(self):
        """Test size before/after calculation"""
        input_data = JSONInput(text=self.sample_json, minify=False)
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.size_before, len(self.sample_json))
        self.assertEqual(result.size_after, len(result.formatted))
        self.assertGreater(result.size_after, result.size_before)  # Formatted is larger
    
    def test_unicode_json(self):
        """Test JSON with Unicode characters"""
        unicode_json = '{"message":"Hello 世界! 🌍","emoji":"🎉"}'
        input_data = JSONInput(text=unicode_json, minify=False)
        result = self.tool.execute(input_data)
        
        self.assertTrue(result.valid)
        self.assertIn("世界", result.formatted)
        self.assertIn("🌍", result.formatted)
        
        # Should parse correctly
        parsed = json.loads(result.formatted)
        self.assertEqual(parsed["message"], "Hello 世界! 🌍")
    
    def test_roundtrip_format_minify(self):
        """Test formatting then minifying returns compact JSON"""
        # Format first
        format_input = JSONInput(text=self.sample_json, minify=False)
        format_result = self.tool.execute(format_input)
        
        # Then minify
        minify_input = JSONInput(text=format_result.formatted, minify=True)
        minify_result = self.tool.execute(minify_input)
        
        # Should be valid and compact
        self.assertTrue(minify_result.valid)
        parsed_original = json.loads(self.sample_json)
        parsed_final = json.loads(minify_result.formatted)
        self.assertEqual(parsed_original, parsed_final)
    
    def test_get_schemas(self):
        """Test schema generation"""
        input_schema = self.tool.get_input_schema()
        output_schema = self.tool.get_output_schema()
        
        self.assertIn("properties", input_schema)
        self.assertIn("text", input_schema["properties"])
        self.assertIn("minify", input_schema["properties"])
        
        self.assertIn("properties", output_schema)
        self.assertIn("formatted", output_schema["properties"])


if __name__ == "__main__":
    unittest.main()