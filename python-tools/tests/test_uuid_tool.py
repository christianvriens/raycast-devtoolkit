#!/usr/bin/env python3
"""
Test UUID Tool Plugin
Tests the UUID generation functionality
"""

import unittest
import sys
import os
import uuid
import re

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins.uuid_tool import UUIDTool, UUIDInput


class TestUUIDTool(unittest.TestCase):
    """Test cases for UUID tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tool = UUIDTool()
        self.uuid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    
    def test_tool_config(self):
        """Test tool configuration"""
        config = self.tool.get_config()
        self.assertEqual(config.name, "uuid")
        self.assertEqual(config.category, "text")
        self.assertIn("uuid", config.keywords)
    
    def test_uuid_v4_generation(self):
        """Test UUID v4 generation"""
        input_data = UUIDInput(version=4, count=1)
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.version, 4)
        self.assertEqual(result.count, 1)
        self.assertEqual(len(result.uuids), 1)
        
        # Should be valid UUID format
        generated_uuid = result.uuids[0]
        self.assertTrue(self.uuid_pattern.match(generated_uuid))
        
        # UUID v4 should have '4' in the version position
        self.assertEqual(generated_uuid[14], '4')
    
    def test_uuid_v1_generation(self):
        """Test UUID v1 generation"""
        input_data = UUIDInput(version=1, count=1)
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.version, 1)
        self.assertEqual(result.count, 1)
        self.assertEqual(len(result.uuids), 1)
        
        # Should be valid UUID format
        generated_uuid = result.uuids[0]
        self.assertTrue(self.uuid_pattern.match(generated_uuid))
        
        # UUID v1 should have '1' in the version position
        self.assertEqual(generated_uuid[14], '1')
    
    def test_multiple_uuid_generation(self):
        """Test generating multiple UUIDs"""
        input_data = UUIDInput(version=4, count=5)
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.count, 5)
        self.assertEqual(len(result.uuids), 5)
        
        # All should be valid and unique
        for generated_uuid in result.uuids:
            self.assertTrue(self.uuid_pattern.match(generated_uuid))
        
        # Should be unique (very high probability)
        unique_uuids = set(result.uuids)
        self.assertEqual(len(unique_uuids), 5)
    
    def test_invalid_version(self):
        """Test handling invalid UUID version"""
        with self.assertRaises(Exception):
            UUIDInput(version=3, count=1)  # Only 1 and 4 supported
    
    def test_invalid_count(self):
        """Test handling invalid count"""
        with self.assertRaises(Exception):
            UUIDInput(version=4, count=0)  # Must be positive
        
        with self.assertRaises(Exception):
            UUIDInput(version=4, count=101)  # Too many
    
    def test_default_values(self):
        """Test default input values"""
        input_data = UUIDInput()  # Should use defaults
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.version, 4)  # Default version
        self.assertEqual(result.count, 1)    # Default count
        self.assertEqual(len(result.uuids), 1)
    
    def test_uuid_format_consistency(self):
        """Test UUID format is consistent"""
        input_data = UUIDInput(version=4, count=10)
        result = self.tool.execute(input_data)
        
        for generated_uuid in result.uuids:
            # Check format
            self.assertTrue(self.uuid_pattern.match(generated_uuid))
            # Check length
            self.assertEqual(len(generated_uuid), 36)  # 32 chars + 4 hyphens
            # Check hyphen positions
            self.assertEqual(generated_uuid[8], '-')
            self.assertEqual(generated_uuid[13], '-')
            self.assertEqual(generated_uuid[18], '-')
            self.assertEqual(generated_uuid[23], '-')
    
    def test_uuid_parsability(self):
        """Test generated UUIDs can be parsed by Python's uuid module"""
        input_data = UUIDInput(version=4, count=3)
        result = self.tool.execute(input_data)
        
        for generated_uuid in result.uuids:
            # Should be parsable by Python's uuid module
            parsed_uuid = uuid.UUID(generated_uuid)
            self.assertEqual(str(parsed_uuid), generated_uuid)
            self.assertEqual(parsed_uuid.version, 4)
    
    def test_get_schemas(self):
        """Test schema generation"""
        input_schema = self.tool.get_input_schema()
        output_schema = self.tool.get_output_schema()
        
        self.assertIn("properties", input_schema)
        self.assertIn("version", input_schema["properties"])
        self.assertIn("count", input_schema["properties"])
        
        self.assertIn("properties", output_schema)
        self.assertIn("uuids", output_schema["properties"])


if __name__ == "__main__":
    unittest.main()