"""
JSON Formatter Plugin
Formats, validates, and minifies JSON strings
"""

import json
from typing import Type, Any, Dict
from pydantic import BaseModel, Field, field_validator

from core.base import BaseTool, ToolInput, ToolOutput, ToolConfig, registry


class JSONInput(ToolInput):
    """Input model for JSON formatting"""
    text: str = Field(description="JSON text to format or minify")
    minify: bool = Field(default=False, description="Whether to minify instead of format")
    auto_unescape: bool = Field(default=True, description="Automatically unescape common encodings (html/json/xml/js) before parsing")
    
    @field_validator('text')
    def text_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("JSON text cannot be empty")
        return v.strip()


class JSONOutput(ToolOutput):
    """Output model for JSON formatting"""
    formatted: str = Field(description="Formatted or minified JSON")
    original: str = Field(description="Original input")
    operation: str = Field(description="Operation performed (format/minify)")
    valid: bool = Field(description="Whether input was valid JSON")
    size_before: int = Field(description="Size before formatting")
    size_after: int = Field(description="Size after formatting")
    parsed_data: Dict[str, Any] = Field(description="Parsed JSON data structure")


class JSONTool(BaseTool):
    """JSON formatter and validator tool"""
    
    def get_config(self) -> ToolConfig:
        return ToolConfig(
            name="json",
            description="Format, validate, and minify JSON strings",
            category="text",
            keywords=["json", "format", "minify", "validate", "pretty", "parse"]
        )
    
    def get_input_model(self) -> Type[ToolInput]:
        return JSONInput
    
    def get_output_model(self) -> Type[ToolOutput]:
        return JSONOutput
    
    def execute(self, input_data: JSONInput) -> JSONOutput:
        """Format or minify JSON"""
        text = input_data.text
        operation = "minify" if input_data.minify else "format"
        # Try parsing JSON first.
        parse_text = text
        try:
            parsed_data = json.loads(parse_text)
        except json.JSONDecodeError:
            # If parsing failed, optionally try a best-effort auto-unescape and parse again
            if input_data.auto_unescape:
                try:
                    from .escape_tool import EscapeTool
                    et = EscapeTool()
                    html_out = et.run({"text": parse_text, "operation": "unescape", "format": "html"})
                    parse_text = html_out.get("output_text", parse_text)
                    js_out = et.run({"text": parse_text, "operation": "unescape", "format": "javascript"})
                    parse_text = js_out.get("output_text", parse_text)
                except Exception:
                    # best-effort: if unescape fails, continue to raise parse error below
                    pass
                try:
                    parsed_data = json.loads(parse_text)
                except json.JSONDecodeError as e:
                    raise ValueError(f"Invalid JSON after auto-unescape: {e}")
            else:
                raise ValueError("Invalid JSON: could not parse input")

        # Format or minify
        if input_data.minify:
            formatted = json.dumps(parsed_data, separators=(',', ':'), ensure_ascii=False)
        else:
            formatted = json.dumps(parsed_data, indent=2, ensure_ascii=False, sort_keys=True)

        return JSONOutput(
            formatted=formatted,
            original=parse_text,
            operation=operation,
            valid=True,
            size_before=len(parse_text),
            size_after=len(formatted),
            parsed_data=parsed_data
        )


# Register the tool
registry.register_tool(JSONTool, 'json')