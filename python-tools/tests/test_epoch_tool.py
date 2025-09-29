#!/usr/bin/env python3
"""
Test Epoch Tool Plugin
Tests the epoch timestamp conversion functionality
"""

import unittest
import sys
import os
import time
from datetime import datetime, timezone

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins.epoch_tool import EpochTool, EpochInput


class TestEpochTool(unittest.TestCase):
    """Test cases for Epoch tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tool = EpochTool()
    
    def test_tool_config(self):
        """Test tool configuration"""
        config = self.tool.get_config()
        self.assertEqual(config.name, "epoch")
        self.assertEqual(config.category, "time")
        self.assertIn("epoch", config.keywords)
    
    def test_current_time_conversion(self):
        """Test converting current time (no input)"""
        input_data = EpochInput()  # No timestamp = current time
        result = self.tool.execute(input_data)
        
        # Should be close to current time
        current_epoch = int(time.time())
        self.assertAlmostEqual(result.epoch, current_epoch, delta=2)  # Within 2 seconds
        
        # Should have all format fields
        self.assertIn("readable", result.utc)
        self.assertIn("iso", result.utc)
        self.assertIn("ddmmyyyy", result.utc)
        self.assertIn("readable", result.local)
        self.assertIn("days", result.relative)
        self.assertIn("seconds", result.relative)
        self.assertIn("human", result.relative)
    
    def test_specific_timestamp_conversion(self):
        """Test converting specific timestamp"""
        # Jan 1, 2020 00:00:00 UTC
        test_epoch = "1577836800"
        input_data = EpochInput(timestamp=test_epoch)
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.epoch, 1577836800)
        self.assertIn("2020-01-01", result.utc["readable"])
        self.assertIn("2020-01-01T00:00:00", result.utc["iso"])
        self.assertIn("01/01/2020", result.utc["ddmmyyyy"])
    
    def test_millisecond_timestamp(self):
        """Test converting millisecond timestamp"""
        # Millisecond timestamp (13+ digits)
        ms_timestamp = "1577836800000"  # Same as above but in ms
        input_data = EpochInput(timestamp=ms_timestamp)
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.epoch, 1577836800)  # Should convert ms to seconds
        self.assertIn("2020-01-01", result.utc["readable"])
    
    def test_invalid_timestamp(self):
        """Test handling invalid timestamp"""
        with self.assertRaises(ValueError):
            input_data = EpochInput(timestamp="not_a_number")
            self.tool.execute(input_data)
    
    def test_empty_timestamp(self):
        """Test handling empty timestamp"""
        input_data = EpochInput(timestamp="")
        result = self.tool.execute(input_data)
        
        # Should use current time
        current_epoch = int(time.time())
        self.assertAlmostEqual(result.epoch, current_epoch, delta=2)
    
    def test_relative_time_calculation(self):
        """Test relative time calculation"""
        # Use a timestamp from 1 day ago
        one_day_ago = int(time.time()) - 86400  # 86400 seconds = 1 day
        input_data = EpochInput(timestamp=str(one_day_ago))
        result = self.tool.execute(input_data)
        
        self.assertAlmostEqual(result.relative["days"], 1, delta=0.1)
        self.assertAlmostEqual(result.relative["seconds"], 86400, delta=60)  # Within a minute
        self.assertIn("ago", result.relative["human"])
    
    def test_future_timestamp(self):
        """Test future timestamp handling"""
        # Use a timestamp 1 hour in the future
        one_hour_future = int(time.time()) + 3600  # 3600 seconds = 1 hour
        input_data = EpochInput(timestamp=str(one_hour_future))
        result = self.tool.execute(input_data)
        
        self.assertLess(result.relative["days"], 0)  # Negative days for future
        self.assertLess(result.relative["seconds"], 0)  # Negative seconds for future
        self.assertIn("from now", result.relative["human"])
    
    def test_various_time_formats(self):
        """Test various relative time format outputs"""
        current_time = int(time.time())
        
        # Test seconds ago
        seconds_ago = current_time - 30
        input_data = EpochInput(timestamp=str(seconds_ago))
        result = self.tool.execute(input_data)
        self.assertIn("seconds ago", result.relative["human"])
        
        # Test minutes ago
        minutes_ago = current_time - 300  # 5 minutes
        input_data = EpochInput(timestamp=str(minutes_ago))
        result = self.tool.execute(input_data)
        self.assertIn("minutes ago", result.relative["human"])
        
        # Test hours ago
        hours_ago = current_time - 7200  # 2 hours
        input_data = EpochInput(timestamp=str(hours_ago))
        result = self.tool.execute(input_data)
        self.assertIn("hours ago", result.relative["human"])
    
    def test_timezone_handling(self):
        """Test timezone handling in output"""
        test_epoch = "1577836800"  # Jan 1, 2020 00:00:00 UTC
        input_data = EpochInput(timestamp=test_epoch)
        result = self.tool.execute(input_data)
        
        # UTC should have UTC in readable format
        self.assertIn("UTC", result.utc["readable"])
        
        # Local time should be different from UTC (unless running in UTC timezone)
        # ISO formats should be properly formatted
        self.assertTrue(result.utc["iso"].endswith("+00:00") or result.utc["iso"].endswith("Z"))
    
    def test_get_schemas(self):
        """Test schema generation"""
        input_schema = self.tool.get_input_schema()
        output_schema = self.tool.get_output_schema()
        
        self.assertIn("properties", input_schema)
        self.assertIn("timestamp", input_schema["properties"])
        
        self.assertIn("properties", output_schema)
        self.assertIn("epoch", output_schema["properties"])
        self.assertIn("utc", output_schema["properties"])
        self.assertIn("local", output_schema["properties"])


if __name__ == "__main__":
    unittest.main()