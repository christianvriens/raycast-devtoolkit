# DevToolkit Developer Guide

Complete guide for developing plugins and extending the DevToolkit architecture.

## 🏗 Architecture Overview

DevToolkit uses a **dual plugin architecture** with TypeScript frontend and Python backend components:

```
┌─────────────────────┐    ┌─────────────────────┐
│   TypeScript        │    │      Python         │
│   Frontend          │    │      Backend        │
│                     │    │                     │
│ ┌─────────────────┐ │    │ ┌─────────────────┐ │
│ │ Plugin Registry │ │    │ │  Tool Registry  │ │
│ │  - Discovery    │ │    │ │  - Factory      │ │
│ │  - Management   │ │    │ │  - Validation   │ │
│ └─────────────────┘ │    │ └─────────────────┘ │
│                     │    │                     │
│ ┌─────────────────┐ │    │ ┌─────────────────┐ │
│ │ Base Components │ │    │ │   Base Tools    │ │
│ │  - Forms        │ │    │ │  - Models       │ │
│ │  - Hooks        │ │    │ │  - Validation   │ │
│ └─────────────────┘ │    │ └─────────────────┘ │
└─────────────────────┘    └─────────────────────┘
           │                           │
           └───────────────────────────┘
                      JSON API
```

## 🔧 Creating a New Plugin

### Step 1: Python Backend Plugin

Create a new Python plugin in `python-tools/plugins/`:

```python
# python-tools/plugins/example_tool.py
"""
Example Tool Plugin
Demonstrates plugin development patterns
"""

from typing import Type, Optional
from pydantic import BaseModel, Field, validator
from core.base import BaseTool, ToolInput, ToolOutput, ToolConfig, registry


class ExampleInput(ToolInput):
    """Input model with validation"""
    text: str = Field(description="Input text to process")
    option: str = Field(default="default", description="Processing option")
    
    @validator('text')
    def text_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Text cannot be empty")
        return v.strip()
    
    @validator('option')
    def valid_option(cls, v):
        valid_options = ["default", "uppercase", "reverse"]
        if v not in valid_options:
            raise ValueError(f"Option must be one of: {valid_options}")
        return v


class ExampleOutput(ToolOutput):
    """Structured output model"""
    input: str = Field(description="Original input")
    output: str = Field(description="Processed output")
    option_used: str = Field(description="Option applied")
    length: int = Field(description="Output length")


class ExampleTool(BaseTool):
    """Example tool implementation"""
    
    def get_config(self) -> ToolConfig:
        return ToolConfig(
            name="example",
            description="Example tool for demonstration",
            category="text",
            version="1.0.0",
            author="DevToolkit",
            keywords=["example", "demo", "text", "processing"]
        )
    
    def get_input_model(self) -> Type[ToolInput]:
        return ExampleInput
    
    def get_output_model(self) -> Type[ToolOutput]:
        return ExampleOutput
    
    def execute(self, input_data: ExampleInput) -> ExampleOutput:
        """Execute the tool logic"""
        text = input_data.text
        option = input_data.option
        
        # Process based on option
        if option == "uppercase":
            processed = text.upper()
        elif option == "reverse":
            processed = text[::-1]
        else:
            processed = text
        
        return ExampleOutput(
            input=text,
            output=processed,
            option_used=option,
            length=len(processed)
        )


# Auto-register the tool
registry.register_tool(ExampleTool, 'example')
```

### Step 2: Update Plugin Registry

Add your plugin to `python-tools/plugins/__init__.py`:

```python
"""
DevToolkit Plugins
Auto-import all available plugins
"""

# Import all plugin modules to trigger registration
from . import base64_tool
from . import url_tool
from . import hash_tool
from . import jwt_tool
from . import json_tool
from . import uuid_tool
from . import epoch_tool
from . import color_tool
from . import example_tool  # Add your plugin

__all__ = [
    'base64_tool',
    'url_tool', 
    'hash_tool',
    'jwt_tool',
    'json_tool',
    'uuid_tool',
    'epoch_tool',
    'color_tool',
    'example_tool',  # Add your plugin
]
```

### Step 3: TypeScript Frontend Plugin

Create the TypeScript component in `src/plugins/`:

```tsx
// src/plugins/text/example.tsx
/**
 * Example Plugin
 * Demonstrates frontend plugin patterns
 */

import { Icon, Form } from "@raycast/api";
import { useState } from "react";
import { PluginDefinition } from "../types";
import { BaseForm } from "../base";
import { PythonTools, DevToolsUtils } from "../../python-tools";

// Example Tool Component
function ExampleTool() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const process = async (values: { text: string; option: string }) => {
    setIsLoading(true);
    
    try {
      // Call Python tool via legacy API or create new method
      const data = await executePythonTool("example", [
        values.text, 
        "--option", 
        values.option
      ]);
      
      setResult(data.output);
      
      // Auto-copy and show success
      await DevToolsUtils.copyToClipboard(
        data.output, 
        `Text processed with ${values.option} option`
      );
      
    } catch (error) {
      await DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <BaseForm
      title="Example Tool"
      onSubmit={process}
      isLoading={isLoading}
      result={result}
      submitButtonTitle="Process Text"
      copyButtonTitle="Copy Result"
    >
      <Form.TextArea
        id="text"
        title="Input Text"
        placeholder="Enter text to process"
      />
      <Form.Dropdown id="option" title="Processing Option" defaultValue="default">
        <Form.Dropdown.Item value="default" title="Default" />
        <Form.Dropdown.Item value="uppercase" title="Uppercase" />
        <Form.Dropdown.Item value="reverse" title="Reverse" />
      </Form.Dropdown>
      {result && (
        <Form.TextArea
          id="result"
          title="Result"
          value={result}
        />
      )}
    </BaseForm>
  );
}

// Plugin Definition
export const ExamplePlugin: PluginDefinition = {
  id: "example-plugin",
  name: "Example Tools",
  description: "Example plugin for demonstration",
  version: "1.0.0",
  author: "DevToolkit",
  categories: [
    {
      name: "Text & Data",
      icon: Icon.Document,
      key: "text",
    },
  ],
  tools: [
    {
      name: "Example Tool",
      key: "example",
      icon: Icon.Hammer,
      categoryKey: "text",
      description: "Example tool for processing text",
      keywords: ["example", "demo", "text", "processing"],
      component: ExampleTool,
      pythonCommand: "example",
      autoCopy: true,
    },
  ],
};
```

### Step 4: Register TypeScript Plugin

Add to `src/plugins/index.ts`:

```tsx
// Import your plugin
import { ExamplePlugin } from "./text/example";

// Register all plugins
export const plugins = [
  Base64Plugin,
  UrlPlugin,
  HashPlugin,
  JwtPlugin,
  JsonPlugin,
  UuidPlugin,
  TimestampPlugin,
  ColorPlugin,
  ExamplePlugin,  // Add your plugin
];
```

### Step 5: Add Comprehensive Tests

Create test file `python-tools/tests/test_example_tool.py`:

```python
#!/usr/bin/env python3
"""
Test Example Tool Plugin
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from plugins.example_tool import ExampleTool, ExampleInput


class TestExampleTool(unittest.TestCase):
    
    def setUp(self):
        self.tool = ExampleTool()
    
    def test_tool_config(self):
        """Test tool configuration"""
        config = self.tool.get_config()
        self.assertEqual(config.name, "example")
        self.assertEqual(config.category, "text")
    
    def test_default_processing(self):
        """Test default processing"""
        input_data = ExampleInput(text="hello", option="default")
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.output, "hello")
        self.assertEqual(result.option_used, "default")
        self.assertEqual(result.length, 5)
    
    def test_uppercase_processing(self):
        """Test uppercase processing"""
        input_data = ExampleInput(text="hello", option="uppercase")
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.output, "HELLO")
        self.assertEqual(result.option_used, "uppercase")
    
    def test_reverse_processing(self):
        """Test reverse processing"""
        input_data = ExampleInput(text="hello", option="reverse")
        result = self.tool.execute(input_data)
        
        self.assertEqual(result.output, "olleh")
        self.assertEqual(result.option_used, "reverse")
    
    def test_empty_text_validation(self):
        """Test empty text validation"""
        with self.assertRaises(ValueError):
            ExampleInput(text="", option="default")
    
    def test_invalid_option_validation(self):
        """Test invalid option validation"""
        with self.assertRaises(ValueError):
            ExampleInput(text="hello", option="invalid")
    
    def test_schema_generation(self):
        """Test schema generation"""
        input_schema = self.tool.get_input_schema()
        output_schema = self.tool.get_output_schema()
        
        self.assertIn("properties", input_schema)
        self.assertIn("properties", output_schema)


if __name__ == "__main__":
    unittest.main()
```

## 📋 Plugin Development Checklist

### Python Plugin Requirements
- [ ] Inherits from `BaseTool`
- [ ] Implements `get_config()` with proper metadata
- [ ] Defines input/output models with Pydantic
- [ ] Implements `execute()` method with business logic
- [ ] Includes proper validation with `@validator` decorators
- [ ] Auto-registers with `registry.register_tool()`
- [ ] Added to `plugins/__init__.py`

### TypeScript Plugin Requirements
- [ ] Creates React component with form inputs
- [ ] Implements proper error handling
- [ ] Includes auto-copy functionality
- [ ] Defines `PluginDefinition` with metadata
- [ ] Registered in `src/plugins/index.ts`
- [ ] Uses consistent UI patterns from `BaseForm`

### Testing Requirements  
- [ ] Comprehensive test suite created
- [ ] Tests cover all functionality and edge cases
- [ ] Tests include validation scenarios
- [ ] Tests verify schema generation
- [ ] All tests pass with 100% success rate

## 🎨 UI Patterns

### Form Components

```tsx
// Basic form with text input
<Form.TextField
  id="text"
  title="Input Text"
  placeholder="Enter text here"
/>

// Text area for larger content
<Form.TextArea
  id="content"
  title="Content"
  placeholder="Paste content here"
/>

// Dropdown for options
<Form.Dropdown id="option" title="Option" defaultValue="default">
  <Form.Dropdown.Item value="option1" title="Option 1" />
  <Form.Dropdown.Item value="option2" title="Option 2" />
</Form.Dropdown>

// Checkbox for boolean options
<Form.Checkbox
  id="enabled"
  title="Feature Enabled"
  label="Enable this feature"
/>

// Display results
{result && (
  <Form.TextArea
    id="result"
    title="Result"
    value={result}
  />
)}
```

### State Management

```tsx
function MyTool() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [warning, setWarning] = useState<string>("");

  const handleSubmit = async (values: FormValues) => {
    setIsLoading(true);
    setWarning("");
    
    try {
      const data = await PythonTools.myTool(values);
      setResult(data.output);
      
      // Check for warnings
      if (data.warning) {
        setWarning(data.warning);
      }
      
      // Auto-copy success
      await DevToolsUtils.copyToClipboard(
        data.output, 
        "Operation completed"
      );
      
    } catch (error) {
      await DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <BaseForm
      title="My Tool"
      onSubmit={handleSubmit}
      isLoading={isLoading}
      result={result}
    >
      {/* Form inputs */}
      {warning && (
        <Form.Description
          title="Warning"
          text={warning}
        />
      )}
    </BaseForm>
  );
}
```

## 🔍 Debugging

### Python Tool Debugging

```bash
# Test individual tools
python3 python-tools/devtools.py info my_tool
python3 python-tools/devtools.py my_tool "test input"

# Run with verbose output
python3 python-tools/devtools.py run my_tool '{"text":"test"}' | jq

# Check tool registration
python3 python-tools/devtools.py list
```

### TypeScript Debugging

```tsx
// Add console logging
console.log(`Executing: ${command} with args:`, args);

// Debug Python tool responses
const data = await PythonTools.myTool(values);
console.log("Python response:", data);
```

## 📚 Best Practices

### Input Validation
- Use Pydantic validators for complex validation
- Provide clear error messages
- Support multiple input formats when appropriate
- Validate early and fail fast

### Output Structure
- Use consistent field naming (input, output, operation)
- Include metadata (length, format, validation status)
- Provide human-readable messages when helpful
- Structure data for easy consumption

### Error Handling
- Catch and handle specific exceptions
- Provide actionable error messages
- Include context in error responses
- Graceful degradation when possible

### Testing Strategy
- Test happy path and edge cases
- Include validation testing
- Test with Unicode and special characters
- Verify schema generation
- Test integration between Python and TypeScript

## 🚀 Advanced Features

### Custom Validation

```python
@validator('email')
def validate_email(cls, v):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, v):
        raise ValueError("Invalid email format")
    return v
```

### Complex Output Models

```python
class AnalysisOutput(ToolOutput):
    results: List[Dict[str, Any]] = Field(description="Analysis results")
    summary: Dict[str, Union[str, int]] = Field(description="Summary statistics")
    warnings: List[str] = Field(default_factory=list, description="Warnings")
    metadata: Dict[str, Any] = Field(description="Processing metadata")
```

### Async Processing

```tsx
// Handle long-running operations
const [progress, setProgress] = useState(0);

const processLargeInput = async (values: FormValues) => {
  setIsLoading(true);
  
  try {
    // Show progress for long operations
    const progressInterval = setInterval(() => {
      setProgress(prev => Math.min(prev + 10, 90));
    }, 100);
    
    const result = await PythonTools.myTool(values);
    clearInterval(progressInterval);
    setProgress(100);
    
    // Handle result
    
  } catch (error) {
    setProgress(0);
    // Handle error
  } finally {
    setIsLoading(false);
    setTimeout(() => setProgress(0), 1000);
  }
};
```

---

**Following these patterns ensures consistent, reliable, and maintainable plugins that integrate seamlessly with the DevToolkit ecosystem.**