"""
Escape / Unescape utilities
Provides tools to escape and unescape HTML, JSON, XML, and JavaScript strings
"""

from typing import Type, Any, Dict
from pydantic import Field

from core.base import BaseTool, ToolInput, ToolOutput, ToolConfig, registry

import html
import json as _json
from xml.sax import saxutils
import re


class EscapeInput(ToolInput):
    text: str = Field(description="Text to escape or unescape")
    operation: str = Field(description="escape or unescape", default="escape")
    format: str = Field(description="format: html|json|xml|javascript", default="html")


class EscapeOutput(ToolOutput):
    input_text: str
    output_text: str
    operation: str
    format: str


class EscapeTool(BaseTool):
    def get_config(self) -> ToolConfig:
        return ToolConfig(
            name="escape",
            description="Escape or unescape text for HTML, JSON, XML or JavaScript",
            category="escape/unescape",
            keywords=["escape", "unescape", "html", "json", "xml", "javascript"],
        )

    def get_input_model(self) -> Type[ToolInput]:
        return EscapeInput

    def get_output_model(self) -> Type[ToolOutput]:
        return EscapeOutput

    def execute(self, input_data: EscapeInput) -> EscapeOutput:
        text = input_data.text
        op = (input_data.operation or "").lower()
        fmt = (input_data.format or "").lower()

        if op not in ("escape", "unescape"):
            raise ValueError("operation must be 'escape' or 'unescape'")
        if fmt not in ("html", "json", "xml", "javascript"):
            raise ValueError("format must be one of: html, json, xml, javascript")

        if fmt == "html":
            if op == "escape":
                out = html.escape(text)
            else:
                out = html.unescape(text)

        elif fmt == "json":
            if op == "escape":
                # Use json encoding to escape
                out = _json.dumps(text, ensure_ascii=False)[1:-1]
            else:
                # Try to decode as a JSON string
                try:
                    out = _json.loads(f'"{text.replace('"', '\\"')}"')
                except Exception:
                    # fallback: unescape common sequences
                    out = text.encode('utf-8').decode('unicode_escape')

        elif fmt == "xml":
            if op == "escape":
                out = saxutils.escape(text)
            else:
                out = saxutils.unescape(text)

        else:  # javascript
            if op == "escape":
                # More complete JS escaping: escape control chars, quotes, backslashes, and non-ascii as \uXXXX
                def js_escape(s: str) -> str:
                    res = []
                    for ch in s:
                        o = ord(ch)
                        if ch == '"':
                            res.append('\\\"')
                        elif ch == "'":
                            res.append("\\'")
                        elif ch == "\\":
                            res.append('\\\\')
                        elif ch == '\n':
                            res.append('\\n')
                        elif ch == '\r':
                            res.append('\\r')
                        elif ch == '\t':
                            res.append('\\t')
                        elif ch == '\b':
                            res.append('\\b')
                        elif ch == '\f':
                            res.append('\\f')
                        elif o < 32:
                            # other control chars
                            res.append('\\u%04x' % o)
                        elif o > 0x7f:
                            # non-ascii -> unicode escape. For codepoints > 0xFFFF produce surrogate pairs
                            if o <= 0xFFFF:
                                res.append('\\u%04x' % o)
                            else:
                                cp = o - 0x10000
                                high = 0xD800 + (cp >> 10)
                                low = 0xDC00 + (cp & 0x3FF)
                                res.append('\\u%04x\\u%04x' % (high, low))
                        else:
                            res.append(ch)
                    return ''.join(res)

                out = js_escape(text)
            else:
                # Unescape JS sequences: \n, \r, \t, \uXXXX, \xXX, \" etc.
                def js_unescape(s: str) -> str:
                    # Replace common escapes
                    s = s.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t')
                    s = s.replace('\\b', '\b').replace('\\f', '\f')
                    s = s.replace('\\\"', '"').replace("\\'", "'").replace('\\\\', '\\')
                    # Handle \xHH
                    def repl_x(m):
                        return chr(int(m.group(1), 16))
                    s = re.sub(r"\\x([0-9a-fA-F]{2})", repl_x, s)

                    # First handle surrogate pairs like \uD83D\uDE00 -> single codepoint
                    def repl_surrogate(m):
                        hi = int(m.group(1), 16)
                        lo = int(m.group(2), 16)
                        cp = ((hi - 0xD800) << 10) + (lo - 0xDC00) + 0x10000
                        return chr(cp)
                    s = re.sub(r"\\u([dD][89abAB][0-9a-fA-F]{2})\\u([dD][cdefCDEF][0-9a-fA-F]{2})", repl_surrogate, s)

                    # Then handle remaining \uHHHH
                    def repl_u(m):
                        return chr(int(m.group(1), 16))
                    s = re.sub(r"\\u([0-9a-fA-F]{4})", repl_u, s)
                    return s

                out = js_unescape(text)

        return EscapeOutput(input_text=text, output_text=out, operation=op, format=fmt)


# Register
registry.register_tool(EscapeTool, 'escape')
