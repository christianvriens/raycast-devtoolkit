# DevToolkit Python Tools

Standalone Python developer utilities with plugin architecture. These tools can be used independently of Raycast or integrated into other applications.

## 🚀 Quick Start

```bash
# List all available tools
python3 devtools.py list

# Get tool information
python3 devtools.py info base64

# Use tools directly
python3 devtools.py base64 "hello world"
python3 devtools.py jwt "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## 📋 Available Tools

| Tool | Command | Description |
|------|---------|-------------|
| **Base64** | `base64` | Encode/decode Base64 strings |
| **URL** | `url` | Encode/decode URL strings with validation |
| **Hash** | `hash` | Generate MD5, SHA1, SHA256, SHA512 hashes |
| **JWT** | `jwt` | Decode and analyze JSON Web Tokens |
| **JSON** | `json` | Format, validate, and minify JSON |
| **UUID** | `uuid` | Generate UUID v1/v4 identifiers |
| **Epoch** | `epoch` | Convert Unix timestamps to readable formats |
| **Color** | `color` | Convert between HEX, RGB, HSL formats |

## 🎯 Usage Examples

### Base64 Tool
```bash
# Encode text
python3 devtools.py base64 "hello world"
# Output: {"input": "hello world", "output": "aGVsbG8gd29ybGQ=", "operation": "encode"}

# Decode base64
python3 devtools.py base64 "aGVsbG8gd29ybGQ=" --decode
# Output: {"input": "aGVsbG8gd29ybGQ=", "output": "hello world", "operation": "decode"}
```

### JWT Tool
```bash
# Decode JWT token
python3 devtools.py jwt "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
# Output: Complete JWT analysis with header, payload, and validation info
```

### Hash Tool
```bash
# Generate SHA256 hash (default)
python3 devtools.py hash "secret"

# Generate MD5 hash
python3 devtools.py hash "secret" --algorithm md5

# Generate SHA512 hash
python3 devtools.py hash "secret" --algorithm sha512
```

### URL Tool
```bash
# URL encode
python3 devtools.py url "hello world"
# Output: {"input": "hello world", "output": "hello%20world", "operation": "encode", "is_valid_url": false}

# URL decode
python3 devtools.py url "hello%20world" --decode
# Output: {"input": "hello%20world", "output": "hello world", "operation": "decode", "is_valid_url": false}
```

### JSON Tool
```bash
# Format JSON
python3 devtools.py json '{"name":"John","age":30}'

# Minify JSON
python3 devtools.py json '{"name": "John", "age": 30}' --minify
```

### UUID Tool
```bash
# Generate UUID v4 (default)
python3 devtools.py uuid

# Generate 5 UUID v4s
python3 devtools.py uuid --count 5

# Generate UUID v1
python3 devtools.py uuid --version 1
```

### Epoch Tool
```bash
# Convert current time
python3 devtools.py epoch

# Convert specific timestamp
python3 devtools.py epoch 1577836800

# Convert millisecond timestamp
python3 devtools.py epoch 1577836800000
```

### Color Tool
```bash
# Convert hex color
python3 devtools.py color "#ff0000"

# Convert RGB color
python3 devtools.py color "rgb(255, 0, 0)"

# Convert HSL color
python3 devtools.py color "hsl(0, 100%, 50%)"
```

## 🏗 Plugin Architecture

### Core Components

```
python-tools/
├── core/
│   ├── __init__.py         # Core exports
│   └── base.py             # Plugin framework
├── plugins/
│   ├── __init__.py         # Auto-import all plugins
│   ├── base64_tool.py      # Base64 plugin
│   ├── url_tool.py         # URL plugin
│   ├── hash_tool.py        # Hash plugin
│   ├── jwt_tool.py         # JWT plugin
│   ├── json_tool.py        # JSON plugin
│   ├── uuid_tool.py        # UUID plugin
│   ├── epoch_tool.py       # Epoch plugin
│   └── color_tool.py       # Color plugin
├── tests/
│   ├── run_all_tests.py    # Test runner
│   └── test_*.py           # Individual plugin tests
├── devtools.py             # CLI interface
└── README.md               # This file
```

### Plugin Development

Each plugin consists of:

1. **Input Model** (Pydantic validation)
2. **Output Model** (Structured response)
3. **Tool Class** (Business logic)
4. **Configuration** (Metadata and keywords)

Example plugin structure:

```python
from core.base import BaseTool, ToolInput, ToolOutput, ToolConfig, registry
from pydantic import BaseModel, Field

class MyToolInput(ToolInput):
    text: str = Field(description="Input text")

class MyToolOutput(ToolOutput):
    result: str = Field(description="Processed result")

class MyTool(BaseTool):
    def get_config(self) -> ToolConfig:
        return ToolConfig(
            name="my_tool",
            description="My custom tool",
            category="custom",
            keywords=["my", "tool", "custom"]
        )
    
    def get_input_model(self) -> Type[ToolInput]:
        return MyToolInput
    
    def get_output_model(self) -> Type[ToolOutput]:
        return MyToolOutput
    
    def execute(self, input_data: MyToolInput) -> MyToolOutput:
        # Tool logic here
        return MyToolOutput(result=f"Processed: {input_data.text}")

# Auto-register the tool
registry.register_tool(MyTool, 'my_tool')
```

## 🧪 Testing

### Run All Tests
```bash
python3 tests/run_all_tests.py
```

### Run Specific Tool Tests
```bash
python3 tests/test_base64_tool.py
python3 tests/test_jwt_tool.py
python3 tests/test_hash_tool.py
```

### Test Coverage
- **77+ comprehensive tests** across all plugins
- **Edge case testing** (empty inputs, invalid data)
- **Unicode support** testing
- **Validation testing** (Pydantic models)
- **Schema generation** testing
- **Roundtrip testing** (encode/decode consistency)

## 🔧 Advanced Usage

### Modern Plugin API
```bash
# Use the modern plugin API
python3 devtools.py run base64 '{"text":"hello","operation":"encode"}'
python3 devtools.py run jwt '{"token":"eyJ..."}'
python3 devtools.py run hash '{"text":"secret","algorithm":"sha256"}'
```

### Tool Information
```bash
# Get tool configuration
python3 devtools.py info base64

# List tools by category
python3 devtools.py list
```

### Integration Example
```python
from python_tools.core import registry

# Get a tool instance
base64_tool = registry.get_tool('base64')

# Execute with validation
input_data = base64_tool.validate_input({"text": "hello", "operation": "encode"})
result = base64_tool.execute(input_data)
print(result.output)  # "aGVsbG8="
```

## 📚 API Documentation

### CLI Commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| `list` | - | List all available tools |
| `info <tool>` | tool name | Get detailed tool information |
| `run <tool> <json>` | tool name, JSON input | Execute tool with modern API |
| `<tool> <args>` | tool-specific | Execute tool with legacy API |

### Tool Categories

- **encoding**: Base64, URL tools
- **security**: Hash, JWT tools  
- **text**: JSON, UUID tools
- **time**: Epoch tools
- **design**: Color tools

## 🔗 Integration

These tools are designed to be:
- **Framework agnostic**: Use with any Python application
- **CLI friendly**: Perfect for shell scripts and automation
- **API ready**: JSON input/output for web services
- **Type safe**: Pydantic validation ensures data integrity

## 📄 Requirements

- **Python 3.7+**
- **pydantic >= 2.0**
- **Standard library modules** (json, hashlib, uuid, etc.)

## 📚 Documentation

### Sphinx Documentation Setup

This project includes comprehensive API documentation built with Sphinx.

#### Installation
```bash
# Install documentation dependencies
pip install -r requirements-docs.txt

# Or install individually
pip install sphinx>=4.0.0 sphinx_rtd_theme>=1.0.0 sphinxcontrib-apidoc>=0.3.0
```

#### Building Documentation
```bash
# Build all documentation (HTML + Sphinx)
./build-docs.sh

# Or build manually from python-tools directory:
cd python-tools/docs
sphinx-build -b html . _build/html

# For live reload during development
sphinx-autobuild . _build/html
```

**Note:** The build script (`./build-docs.sh`) automatically copies the generated Sphinx documentation from `python-tools/docs/_build/html/` to `docs/api/` for centralized project documentation access.

#### View the Documentation

After building, the documentation is available in two locations:

```bash
# Main documentation location (copied by build script)
open ***REMOVED***/Documents/raycast/devtoolkit/docs/api/index.html

# Source documentation location (generated by Sphinx)
open ***REMOVED***/Documents/raycast/devtoolkit/python-tools/docs/_build/html/index.html
```

**Documentation Structure:**
- `docs/api/` - **Main documentation** (copied from Sphinx build for centralized access)
- `python-tools/docs/_build/html/` - **Source documentation** (generated directly by Sphinx)

Both locations contain the same content; `docs/api/` is the canonical location for accessing documentation.

#### Generated Documentation

The documentation system creates:
- **HTML Documentation**: Professional API docs with Read the Docs theme
- **API Reference**: Auto-generated from docstrings and type hints
- **Tool Guides**: Comprehensive examples and usage patterns
- **Architecture Overview**: Plugin system documentation

#### Accessing Documentation
```bash
# Recommended: Open main documentation
open docs/api/index.html

# Development: Open source documentation
open python-tools/docs/_build/html/index.html

# Build and view in one command
./build-docs.sh && open docs/api/index.html
```

#### Documentation Structure

**Project Documentation Layout:**
```
devtoolkit/
├── docs/
│   ├── api/                     # 📍 Main Sphinx documentation (copied)
│   │   ├── index.html           # Primary access point
│   │   ├── quickstart.html      # Quick start guide
│   │   └── tools.html           # Tool reference
│   ├── USER_GUIDE.md            # End-user documentation
│   └── DEVELOPER_GUIDE.md       # Plugin development guide
└── python-tools/
    └── docs/
        ├── conf.py              # Sphinx configuration
        ├── index.rst            # Source documentation files
        └── _build/html/         # 🔧 Generated Sphinx output
            └── index.html       # Source location
```

**Access Points:**
- **Main**: `docs/api/index.html` (recommended)
- **Source**: `python-tools/docs/_build/html/index.html` (development)

#### Customizing Documentation

1. **Configuration**: Edit `docs/conf.py`
2. **Content**: Modify `.rst` files in `docs/`
3. **Theme**: Currently using `sphinx_rtd_theme`
4. **Auto-generation**: API docs generated from code

#### Documentation Features
- ✅ **Auto-generated API reference** from docstrings
- ✅ **Cross-references** between modules and classes
- ✅ **Code examples** with syntax highlighting
- ✅ **Search functionality** built-in
- ✅ **Mobile-responsive** Read the Docs theme
- ✅ **PDF export** capability (with additional setup)

## 🤝 Contributing

1. Create a new plugin in `plugins/`
2. Add comprehensive tests in `tests/`
3. Update plugin imports in `plugins/__init__.py`
4. Ensure all tests pass
5. Submit a pull request

---

**Professional developer tools with enterprise-grade validation and testing**