"""
Hash Tool Plugin
Provides cryptographic hash generation functionality
"""

import hashlib
from typing import Type, Literal
from pydantic import Field, validator
from core import BaseTool, ToolInput, ToolOutput, ToolConfig


class HashInput(ToolInput):
    """Input model for hash operations"""
    text: str = Field(description="Text to hash")
    algorithm: Literal["md5", "sha1", "sha256", "sha512"] = Field(
        default="sha256",
        description="Hash algorithm to use"
    )
    
    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v


class HashOutput(ToolOutput):
    """Output model for hash operations"""
    input: str = Field(description="Original input text")
    algorithm: str = Field(description="Hash algorithm used")
    hash: str = Field(description="Generated hash")
    length: int = Field(description="Hash length in characters")


class HashTool(BaseTool):
    """Cryptographic hash generation tool"""
    
    def get_config(self) -> ToolConfig:
        return ToolConfig(
            name="hash",
            description="Generate cryptographic hashes using various algorithms",
            category="security",
            keywords=["hash", "md5", "sha1", "sha256", "sha512", "crypto", "checksum", "digest"]
        )
    
    def get_input_model(self) -> Type[ToolInput]:
        return HashInput
    
    def get_output_model(self) -> Type[ToolOutput]:
        return HashOutput
    
    def execute(self, input_data: HashInput) -> HashOutput:
        """Execute hash generation"""
        try:
            # Get the appropriate hash function
            algorithms = {
                "md5": hashlib.md5,
                "sha1": hashlib.sha1,
                "sha256": hashlib.sha256,
                "sha512": hashlib.sha512
            }
            
            hash_func = algorithms[input_data.algorithm]()
            hash_func.update(input_data.text.encode('utf-8'))
            hash_value = hash_func.hexdigest()
            
            return HashOutput(
                input=input_data.text,
                algorithm=input_data.algorithm,
                hash=hash_value,
                length=len(hash_value)
            )
        except Exception as e:
            raise ValueError(f"Hash generation failed: {str(e)}")


# Register the tool
from core import registry
registry.register_tool(HashTool)