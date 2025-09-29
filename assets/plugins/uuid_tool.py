"""
UUID Generator Plugin
Generates UUID v1 or v4 identifiers
"""

import uuid
from typing import Type, List
from pydantic import BaseModel, Field, validator

from core.base import BaseTool, ToolInput, ToolOutput, ToolConfig, registry


class UUIDInput(ToolInput):
    """Input model for UUID generation"""
    version: int = Field(default=4, description="UUID version (1 or 4)")
    count: int = Field(default=1, description="Number of UUIDs to generate")
    
    @validator('version')
    def version_must_be_valid(cls, v):
        if v not in [1, 4]:
            raise ValueError("UUID version must be 1 or 4")
        return v
    
    @validator('count')
    def count_must_be_positive(cls, v):
        if v < 1 or v > 100:
            raise ValueError("Count must be between 1 and 100")
        return v


class UUIDOutput(ToolOutput):
    """Output model for UUID generation"""
    uuids: List[str] = Field(description="Generated UUIDs")
    version: int = Field(description="UUID version used")
    count: int = Field(description="Number of UUIDs generated")
    format: str = Field(description="UUID format")


class UUIDTool(BaseTool):
    """UUID generator tool for creating unique identifiers"""
    
    def get_config(self) -> ToolConfig:
        return ToolConfig(
            name="uuid",
            description="Generate UUID v1 or v4 unique identifiers",
            category="text",
            keywords=["uuid", "guid", "identifier", "unique", "random", "generate"]
        )
    
    def get_input_model(self) -> Type[ToolInput]:
        return UUIDInput
    
    def get_output_model(self) -> Type[ToolOutput]:
        return UUIDOutput
    
    def execute(self, input_data: UUIDInput) -> UUIDOutput:
        """Generate UUIDs"""
        uuids = []
        
        for _ in range(input_data.count):
            if input_data.version == 1:
                generated_uuid = str(uuid.uuid1())
            else:  # version 4
                generated_uuid = str(uuid.uuid4())
            
            uuids.append(generated_uuid)
        
        return UUIDOutput(
            uuids=uuids,
            version=input_data.version,
            count=len(uuids),
            format="8-4-4-4-12 hexadecimal digits"
        )


# Register the tool
registry.register_tool(UUIDTool, 'uuid')