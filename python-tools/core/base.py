"""
Base Tool Classes and Interfaces
Defines the foundation for all DevToolkit plugins
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type, Union, get_type_hints
from pydantic import BaseModel, Field

# Pydantic v2 ConfigDict availability check
try:
    from pydantic import ConfigDict
    _HAS_CONFIGDICT = True
except Exception:
    ConfigDict = None
    _HAS_CONFIGDICT = False
import json


class ToolInput(BaseModel):
    """Base class for tool input validation"""
    # Pydantic v2 configuration (set at definition time)
    if _HAS_CONFIGDICT:
        model_config = ConfigDict(extra="allow")
    else:
        class Config:
            extra = "allow"


class ToolOutput(BaseModel):
    """Base class for tool output structure"""
    # Pydantic v2 configuration for JSON encoders
    if _HAS_CONFIGDICT:
        model_config = ConfigDict(json_encoders={
            # Add custom encoders if needed
        })
    else:
        class Config:
            json_encoders = {
                # Add custom encoders if needed
            }


class ToolConfig(BaseModel):
    """Configuration options for a tool"""
    name: str = Field(description="Tool name")
    description: str = Field(description="Tool description")
    category: str = Field(description="Tool category")
    version: str = Field(default="1.0.0", description="Tool version")
    author: str = Field(default="DevToolkit", description="Tool author")
    keywords: List[str] = Field(default_factory=list, description="Search keywords")


class BaseTool(ABC):
    """Abstract base class for all DevToolkit plugins"""
    
    def __init__(self):
        self._config = self.get_config()
    
    @property
    def config(self) -> ToolConfig:
        """Get tool configuration"""
        return self._config
    
    @abstractmethod
    def get_config(self) -> ToolConfig:
        """Return tool configuration"""
        pass
    
    @abstractmethod
    def get_input_model(self) -> Type[ToolInput]:
        """Return the Pydantic model for input validation"""
        pass
    
    @abstractmethod
    def get_output_model(self) -> Type[ToolOutput]:
        """Return the Pydantic model for output structure"""
        pass
    
    @abstractmethod
    def execute(self, input_data: ToolInput) -> ToolOutput:
        """Execute the tool with validated input"""
        pass
    
    def get_input_schema(self) -> Dict[str, Any]:
        """Get JSON schema for input validation"""
        return self.get_input_model().model_json_schema()
    
    def get_output_schema(self) -> Dict[str, Any]:
        """Get JSON schema for output structure"""
        return self.get_output_model().model_json_schema()
    
    def validate_input(self, data: Dict[str, Any]) -> ToolInput:
        """Validate and parse input data"""
        input_model = self.get_input_model()
        return input_model.model_validate(data)
    
    def format_output(self, output: ToolOutput) -> Dict[str, Any]:
        """Format output as dictionary"""
        return output.model_dump()
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Complete workflow: validate input, execute, format output"""
        try:
            validated_input = self.validate_input(input_data)
            result = self.execute(validated_input)
            return self.format_output(result)
        except Exception as e:
            return {
                "error": str(e),
                "type": type(e).__name__,
                "tool": self.config.name
            }


class ToolRegistry:
    """Factory for registering and managing tools"""
    
    def __init__(self):
        self._tools: Dict[str, Type[BaseTool]] = {}
    
    def register_tool(self, cls: Type[BaseTool], name: str = None) -> None:
        """Register a tool class"""
        if name is None:
            name = cls.__name__.lower().replace('tool', '')
        
        if name in self._tools:
            raise ValueError(f"Tool '{name}' is already registered")
        
        # Validate that the class implements required methods
        if not issubclass(cls, BaseTool):
            raise ValueError(f"Tool '{name}' must inherit from BaseTool")
        
        self._tools[name] = cls
        # Silent registration - no output to avoid interfering with JSON responses
    
    def get_tool(self, name: str) -> BaseTool:
        """Get an instance of a tool"""
        tool_class = self._tools.get(name)
        if tool_class is None:
            raise ValueError(f"Tool '{name}' not found")
        
        return tool_class()
    
    def list_tools(self) -> List[str]:
        """List all registered tool names"""
        return list(self._tools.keys())
    
    def get_tool_info(self, name: str) -> Dict[str, Any]:
        """Get detailed information about a tool"""
        tool = self.get_tool(name)
        return {
            "name": name,
            "config": tool.config.model_dump(),
            "input_schema": tool.get_input_schema(),
            "output_schema": tool.get_output_schema(),
        }
    
    def get_tools_by_category(self, category: str) -> List[str]:
        """Get tools filtered by category"""
        tools = []
        for name in self.list_tools():
            tool = self.get_tool(name)
            if tool.config.category == category:
                tools.append(name)
        return tools
    
    def get_all_categories(self) -> List[str]:
        """Get all unique categories"""
        categories = set()
        for name in self.list_tools():
            tool = self.get_tool(name)
            categories.add(tool.config.category)
        return sorted(list(categories))


# Global registry instance
registry = ToolRegistry()