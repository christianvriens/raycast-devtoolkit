"""
Base64 Tool Plugin
Provides Base64 encoding and decoding functionality
"""

import base64
from typing import Type, Literal
from pydantic import Field, validator
from core import BaseTool, ToolInput, ToolOutput, ToolConfig


class Base64Input(ToolInput):
    """Input model for Base64 operations"""
    text: str = Field(description="Text to encode or decode")
    operation: Literal["encode", "decode"] = Field(
        default="encode", 
        description="Operation to perform"
    )
    
    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v


class Base64Output(ToolOutput):
    """Output model for Base64 operations"""
    input: str = Field(description="Original input text")
    output: str = Field(description="Processed output")
    operation: str = Field(description="Operation performed")


class Base64Tool(BaseTool):
    """Base64 encoding/decoding tool"""
    
    def get_config(self) -> ToolConfig:
        return ToolConfig(
            name="base64",
            description="Encode or decode Base64 strings",
            category="encoding",
            keywords=["base64", "encode", "decode", "encoding"]
        )
    
    def get_input_model(self) -> Type[ToolInput]:
        return Base64Input
    
    def get_output_model(self) -> Type[ToolOutput]:
        return Base64Output
    
    def execute(self, input_data: Base64Input) -> Base64Output:
        """Execute Base64 operation"""
        try:
            if input_data.operation == "decode":
                # Decode from Base64
                decoded = base64.b64decode(input_data.text).decode('utf-8')
                output = decoded
            else:
                # Encode to Base64
                encoded = base64.b64encode(input_data.text.encode('utf-8')).decode('utf-8')
                output = encoded
                
            return Base64Output(
                input=input_data.text,
                output=output,
                operation=input_data.operation
            )
        except Exception as e:
            raise ValueError(f"Base64 {input_data.operation} failed: {str(e)}")


# Register the tool
from core import registry
registry.register_tool(Base64Tool)