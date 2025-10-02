#!/usr/bin/env python3
import unittest
import sys
import os

# Add project path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins.escape_tool import EscapeTool


class TestEscapeXmlAndJsEdgeCases(unittest.TestCase):
    def setUp(self):
        self.tool = EscapeTool()

    def test_escape_xml_entities_and_unescape(self):
        text = "<tag attr=\"value & more\">A & B</tag>"
        res = self.tool.run({"text": text, "operation": "escape", "format": "xml"})
        self.assertIn("&lt;tag", res["output_text"]) 
        # round-trip
        res2 = self.tool.run({"text": res["output_text"], "operation": "unescape", "format": "xml"})
        self.assertEqual(res2["output_text"], text)

    def test_js_escape_unicode_bmp_and_nonbmp(self):
        # BMP char
        bmp = "Ω"  # U+03A9
        out = self.tool.run({"text": bmp, "operation": "escape", "format": "javascript"})["output_text"]
        self.assertTrue('\\u03a9' in out.lower())
        # Non-BMP char (emoji)
        emoji = "\U0001F600"  # grinning face U+1F600
        out2 = self.tool.run({"text": emoji, "operation": "escape", "format": "javascript"})["output_text"]
        # Should be two \uXXXX surrogate escapes
        self.assertRegex(out2, r"\\u[dD][89ab][0-9a-f]{2}\\u[dD][cdef][0-9a-f]{2}")

    def test_js_unescape_x_and_u_sequences(self):
        inp = "Hello\\x21 and unicode \\u03A9 and emoji \\uD83D\\uDE00"
        res = self.tool.run({"text": inp, "operation": "unescape", "format": "javascript"})
        # Should decode \x21 -> ! and \u03A9 -> Ω and surrogate pair -> emoji
        self.assertIn("!", res["output_text"])
        self.assertIn("Ω", res["output_text"])
        self.assertIn("\U0001F600", res["output_text"]) 


if __name__ == '__main__':
    unittest.main()
