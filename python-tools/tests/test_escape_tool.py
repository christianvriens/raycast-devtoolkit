#!/usr/bin/env python3
import unittest
import sys
import os

# Add project path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins.escape_tool import EscapeTool

 
class TestEscapeTool(unittest.TestCase):
    def setUp(self):
        self.tool = EscapeTool()

    def test_escape_html(self):
        res = self.tool.run({"text": "a < b & c", "operation": "escape", "format": "html"})
        self.assertEqual(res["output_text"], "a &lt; b &amp; c")

    def test_unescape_html(self):
        res = self.tool.run({"text": "a &lt; b &amp; c", "operation": "unescape", "format": "html"})
        self.assertEqual(res["output_text"], "a < b & c")

    def test_escape_json_basic(self):
        res = self.tool.run({"text": 'hello "world"', "operation": "escape", "format": "json"})
        self.assertIn('\\"', res["output_text"])  # contains escaped quotes


if __name__ == '__main__':
    unittest.main()

