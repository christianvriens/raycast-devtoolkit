#!/usr/bin/env python3
"""
Test Color Tool Plugin
Tests the color conversion functionality
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins.color_tool import ColorTool, ColorInput


class TestColorTool(unittest.TestCase):
    """Test cases for Color tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.tool = ColorTool()
    
    def test_tool_config(self):
        """Test tool configuration"""
        config = self.tool.get_config()
        self.assertEqual(config.name, "color")
        self.assertEqual(config.category, "design")
        self.assertIn("color", config.keywords)
    
    def test_hex_color_conversion(self):
        """Test hex color conversion"""
        input_data = ColorInput(color="#ff0000")  # Red
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.input_format, "hex")
        self.assertEqual(result.hex, "#ff0000")
        self.assertEqual(result.rgb["r"], 255)
        self.assertEqual(result.rgb["g"], 0)
        self.assertEqual(result.rgb["b"], 0)
        self.assertEqual(result.css_rgb, "rgb(255, 0, 0)")
    
    def test_hex_without_hash(self):
        """Test hex color without # prefix"""
        input_data = ColorInput(color="00ff00")  # Green
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.input_format, "hex")
        self.assertEqual(result.hex, "#00ff00")
        self.assertEqual(result.rgb["r"], 0)
        self.assertEqual(result.rgb["g"], 255)
        self.assertEqual(result.rgb["b"], 0)
    
    def test_short_hex_color(self):
        """Test short hex color conversion"""
        input_data = ColorInput(color="#f0a")  # Pink shorthand
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.hex, "#ff00aa")
        self.assertEqual(result.rgb["r"], 255)
        self.assertEqual(result.rgb["g"], 0)
        self.assertEqual(result.rgb["b"], 170)
    
    def test_rgb_color_conversion(self):
        """Test RGB color conversion"""
        input_data = ColorInput(color="rgb(128, 128, 128)")  # Gray
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.input_format, "rgb")
        self.assertEqual(result.rgb["r"], 128)
        self.assertEqual(result.rgb["g"], 128)
        self.assertEqual(result.rgb["b"], 128)
        self.assertEqual(result.hex, "#808080")
        self.assertEqual(result.css_rgb, "rgb(128, 128, 128)")
    
    def test_hsl_color_conversion(self):
        """Test HSL color conversion"""
        input_data = ColorInput(color="hsl(0, 100%, 50%)")  # Red
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.input_format, "hsl")
        self.assertEqual(result.rgb["r"], 255)
        self.assertEqual(result.rgb["g"], 0)
        self.assertEqual(result.rgb["b"], 0)
        self.assertEqual(result.hex, "#ff0000")
    
    def test_white_color(self):
        """Test white color conversion"""
        input_data = ColorInput(color="#ffffff")
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.rgb["r"], 255)
        self.assertEqual(result.rgb["g"], 255)
        self.assertEqual(result.rgb["b"], 255)
        self.assertEqual(result.hsl["h"], 0)
        self.assertEqual(result.hsl["s"], 0)
        self.assertEqual(result.hsl["l"], 100)
    
    def test_black_color(self):
        """Test black color conversion"""
        input_data = ColorInput(color="#000000")
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.rgb["r"], 0)
        self.assertEqual(result.rgb["g"], 0)
        self.assertEqual(result.rgb["b"], 0)
        self.assertEqual(result.hsl["h"], 0)
        self.assertEqual(result.hsl["s"], 0)
        self.assertEqual(result.hsl["l"], 0)
    
    def test_blue_color_hsl(self):
        """Test blue color HSL conversion"""
        input_data = ColorInput(color="#0000ff")  # Pure blue
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.hsl["h"], 240)  # Blue hue
        self.assertEqual(result.hsl["s"], 100)  # Full saturation
        self.assertEqual(result.hsl["l"], 50)   # 50% lightness
    
    def test_invalid_hex_color(self):
        """Test handling invalid hex color"""
        with self.assertRaises(ValueError):
            input_data = ColorInput(color="#gggggg")  # Invalid hex chars
            self.tool.execute(input_data)
    
    def test_invalid_rgb_color(self):
        """Test handling invalid RGB color"""
        with self.assertRaises(ValueError):
            input_data = ColorInput(color="rgb(300, 128, 128)")  # Value too high
            self.tool.execute(input_data)
    
    def test_invalid_color_format(self):
        """Test handling completely invalid color format"""
        with self.assertRaises(ValueError):
            input_data = ColorInput(color="not_a_color")
            self.tool.execute(input_data)
    
    def test_empty_color(self):
        """Test handling empty color input"""
        with self.assertRaises(Exception):
            ColorInput(color="")
    
    def test_rgb_to_hsl_roundtrip(self):
        """Test RGB to HSL conversion accuracy"""
        colors_to_test = [
            ("#ff0000", 0, 100, 50),    # Red
            ("#00ff00", 120, 100, 50),  # Green
            ("#0000ff", 240, 100, 50),  # Blue
            ("#ffff00", 60, 100, 50),   # Yellow
            ("#ff00ff", 300, 100, 50),  # Magenta
            ("#00ffff", 180, 100, 50),  # Cyan
        ]
        
        for hex_color, expected_h, expected_s, expected_l in colors_to_test:
            input_data = ColorInput(color=hex_color)
            result = self.tool.execute(input_data)
            
            self.assertAlmostEqual(result.hsl["h"], expected_h, delta=1)
            self.assertAlmostEqual(result.hsl["s"], expected_s, delta=1)
            self.assertAlmostEqual(result.hsl["l"], expected_l, delta=1)
    
    def test_css_output_formats(self):
        """Test CSS output format correctness"""
        input_data = ColorInput(color="#8A2BE2")  # Blue Violet
        result = self.tool.execute(input_data)
        
        # CSS formats should be properly formatted
        self.assertTrue(result.css_rgb.startswith("rgb("))
        self.assertTrue(result.css_rgb.endswith(")"))
        self.assertTrue(result.css_hsl.startswith("hsl("))
        self.assertTrue(result.css_hsl.endswith(")"))
        self.assertIn("%", result.css_hsl)  # HSL should have % for S and L
    
    def test_get_schemas(self):
        """Test schema generation"""
        input_schema = self.tool.get_input_schema()
        output_schema = self.tool.get_output_schema()
        
        self.assertIn("properties", input_schema)
        self.assertIn("color", input_schema["properties"])
        
        self.assertIn("properties", output_schema)
        self.assertIn("hex", output_schema["properties"])
        self.assertIn("rgb", output_schema["properties"])
        self.assertIn("hsl", output_schema["properties"])


if __name__ == "__main__":
    unittest.main()