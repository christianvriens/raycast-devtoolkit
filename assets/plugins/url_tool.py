"""
URL Tool Plugin
Provides URL encoding and decoding functionality
"""

from urllib.parse import quote, unquote, urlparse
from typing import Type, Literal
from pydantic import Field, validator
from core import BaseTool, ToolInput, ToolOutput, ToolConfig


class UrlInput(ToolInput):
    """Input model for URL operations"""
    text: str = Field(description="Text or URL to encode or decode")
    operation: Literal["encode", "decode"] = Field(
        default="encode", 
        description="Operation to perform"
    )
    
    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v
    
    @validator('text')
    def validate_url_for_decode(cls, v, values):
        # If decoding, check if it looks like an encoded URL
        if values.get('operation') == 'decode':
            if '%' not in v:
                raise ValueError("Text doesn't appear to be URL encoded (no % characters found)")
        return v


class UrlOutput(ToolOutput):
    """Output model for URL operations"""
    input: str = Field(description="Original input text")
    output: str = Field(description="Processed output")
    operation: str = Field(description="Operation performed")
    is_valid_url: bool = Field(description="Whether the result is a valid URL")


class UrlTool(BaseTool):
    """URL encoding/decoding tool"""
    
    def get_config(self) -> ToolConfig:
        return ToolConfig(
            name="url",
            description="Encode or decode URL strings with validation",
            category="encoding",
            keywords=["url", "encode", "decode", "percent", "encoding", "uri"]
        )
    
    def get_input_model(self) -> Type[ToolInput]:
        return UrlInput
    
    def get_output_model(self) -> Type[ToolOutput]:
        return UrlOutput
    
    def _is_valid_url(self, url: str) -> bool:
        """Check if string is a valid URL"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def execute(self, input_data: UrlInput) -> UrlOutput:
        """Execute URL operation"""
        try:
            if input_data.operation == "decode":
                # Decode URL
                output = unquote(input_data.text)
            else:
                # Encode URL
                output = quote(input_data.text)
            
            # Check if result is a valid URL
            is_valid_url = self._is_valid_url(output if input_data.operation == "decode" else input_data.text)
                
            return UrlOutput(
                input=input_data.text,
                output=output,
                operation=input_data.operation,
                is_valid_url=is_valid_url
            )
        except Exception as e:
            raise ValueError(f"URL {input_data.operation} failed: {str(e)}")


# Register the tool
from core import registry
registry.register_tool(UrlTool)