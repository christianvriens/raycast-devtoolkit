#!/bin/bash

# DevToolkit Documentation Builder
# Generates comprehensive documentation for both Python tools and Raycast extension

set -e

echo "🔨 Building DevToolkit Documentation"
echo "====================================="

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Create docs directory structure if it doesn't exist
mkdir -p docs/api

echo "📚 Building Python Tools Documentation..."

# Check if Sphinx is installed
if ! python3 -c "import sphinx" &> /dev/null; then
    echo "⚠️  Sphinx not found. Installing..."
    pip3 install -r python-tools/requirements-docs.txt
fi

# Navigate to python-tools and build Sphinx docs
cd python-tools/docs

# Initialize Sphinx project if not done
if [ ! -f "_build/html/index.html" ]; then
    echo "🏗️  Building Sphinx documentation..."
    python3 -m sphinx -b html . _build/html
fi

# Copy built docs to main docs folder
echo "📋 Copying Sphinx docs to main documentation..."
cp -r _build/html/* ../../docs/api/

cd ../..

echo "📝 Generating additional documentation..."

# Generate tool usage examples from tests
echo "🧪 Extracting examples from tests..."

# Create API examples from test files
cat > docs/EXAMPLES.md << 'EOF'
# DevToolkit Examples

This document contains practical examples extracted from the comprehensive test suite.

## Base64 Tool Examples

```python
# Basic encoding
from plugins.base64_tool import Base64Tool, Base64Input

tool = Base64Tool()
input_data = Base64Input(text="hello world", operation="encode")
result = tool.execute(input_data)
print(result.output)  # "aGVsbG8gd29ybGQ="

# Basic decoding
input_data = Base64Input(text="aGVsbG8gd29ybGQ=", operation="decode")
result = tool.execute(input_data)
print(result.output)  # "hello world"

# Unicode support
input_data = Base64Input(text="Hello 世界! 🌍", operation="encode")
result = tool.execute(input_data)
# Handles Unicode characters properly
```

## JWT Tool Examples

```python
# Decode JWT token
from plugins.jwt_tool import JWTTool, JWTInput

tool = JWTTool()
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"

input_data = JWTInput(token=token)
result = tool.execute(input_data)

print(result.header)    # {"alg": "HS256", "typ": "JWT"}
print(result.payload)   # {"sub": "1234567890", "name": "John Doe", "iat": 1516239022}
print(result.valid_format)  # True
```

## Hash Tool Examples

```python
# Generate different hashes
from plugins.hash_tool import HashTool, HashInput

tool = HashTool()

# MD5
result = tool.execute(HashInput(text="hello", algorithm="md5"))
print(result.hash)  # "5d41402abc4b2a76b9719d911017c592"

# SHA256 (recommended)
result = tool.execute(HashInput(text="hello", algorithm="sha256"))
print(result.hash)  # "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
```

## URL Tool Examples

```python
# URL encoding with validation
from plugins.url_tool import UrlTool, UrlInput

tool = UrlTool()

# Encode special characters
result = tool.execute(UrlInput(text="hello world", operation="encode"))
print(result.output)      # "hello%20world"
print(result.is_valid_url)  # False (not a URL)

# Encode actual URL
result = tool.execute(UrlInput(text="https://example.com/path?q=hello world", operation="encode"))
print(result.is_valid_url)  # True
```

## Color Tool Examples

```python
# Color format conversion
from plugins.color_tool import ColorTool, ColorInput

tool = ColorTool()

# Convert HEX to all formats
result = tool.execute(ColorInput(color="#ff0000"))
print(result.hex)      # "#ff0000"
print(result.rgb)      # {"r": 255, "g": 0, "b": 0}
print(result.hsl)      # {"h": 0, "s": 100, "l": 50}
print(result.css_rgb)  # "rgb(255, 0, 0)"

# Convert RGB to other formats
result = tool.execute(ColorInput(color="rgb(128, 128, 128)"))
print(result.hex)  # "#808080"
```

## UUID Tool Examples

```python
# Generate UUIDs
from plugins.uuid_tool import UUIDTool, UUIDInput

tool = UUIDTool()

# Single UUID v4 (default)
result = tool.execute(UUIDInput())
print(result.uuids[0])  # "550e8400-e29b-41d4-a716-446655440000"

# Multiple UUIDs
result = tool.execute(UUIDInput(count=3, version=4))
print(len(result.uuids))  # 3
```

## Error Handling Examples

```python
# Validation errors are handled gracefully
try:
    # Empty input
    Base64Input(text="", operation="encode")
except ValueError as e:
    print(f"Validation error: {e}")

try:
    # Invalid JWT
    JWTInput(token="invalid.jwt.token")
    # Will execute but return valid_format: False
except ValueError as e:
    print(f"Validation error: {e}")
```

EOF

echo "🔍 Generating CLI usage documentation..."

# Generate CLI usage examples
cat > docs/CLI_USAGE.md << 'EOF'
# DevToolkit CLI Usage

Complete command-line interface documentation with examples.

## Command Structure

```bash
# Modern plugin API
python3 devtools.py <command> [arguments]

# Available commands:
# - list: Show all tools
# - info <tool>: Show tool information  
# - run <tool> <json>: Execute with JSON input
# - <tool> [args]: Legacy command format
```

## List and Info Commands

```bash
# List all available tools
python3 devtools.py list
# Output: JSON with all tools and categories

# Get tool information
python3 devtools.py info base64
# Output: Complete tool configuration and schemas
```

## Tool-Specific Usage

### Base64 Tool
```bash
# Encode (legacy)
python3 devtools.py base64 "hello world"

# Decode (legacy)  
python3 devtools.py base64 "aGVsbG8gd29ybGQ=" --decode

# Modern API
python3 devtools.py run base64 '{"text":"hello","operation":"encode"}'
```

### JWT Tool
```bash
# Decode JWT (legacy)
python3 devtools.py jwt "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Modern API
python3 devtools.py run jwt '{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}'
```

### Hash Tool
```bash
# Generate SHA256 (default)
python3 devtools.py hash "secret"

# Generate MD5
python3 devtools.py hash "secret" --algorithm md5

# All algorithms: md5, sha1, sha256, sha512
```

### URL Tool  
```bash
# URL encode
python3 devtools.py url "hello world"

# URL decode
python3 devtools.py url "hello%20world" --decode
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
# Generate single UUID v4 (default)
python3 devtools.py uuid

# Generate multiple UUIDs
python3 devtools.py uuid --count 5 --version 4

# Generate UUID v1
python3 devtools.py uuid --version 1
```

### Epoch Tool
```bash
# Convert current time
python3 devtools.py epoch

# Convert specific timestamp
python3 devtools.py epoch 1640995200

# Millisecond timestamp
python3 devtools.py epoch 1640995200000
```

### Color Tool
```bash
# Convert HEX color
python3 devtools.py color "#ff0000"

# Convert RGB color
python3 devtools.py color "rgb(255, 0, 0)"

# Convert HSL color  
python3 devtools.py color "hsl(0, 100%, 50%)"
```

## Automation Examples

```bash
# Batch processing
for text in "hello" "world" "test"; do
    python3 devtools.py base64 "$text"
done

# Process file content
cat data.txt | while read line; do
    python3 devtools.py hash "$line" --algorithm sha256
done

# Generate multiple UUIDs for database
python3 devtools.py uuid --count 10 > uuids.json
```

## Output Format

All tools return structured JSON:

```json
{
  "input": "original input",
  "output": "processed result", 
  "operation": "operation_performed",
  "metadata": {
    "additional": "information"
  }
}
```

## Error Handling

```bash
# Invalid input
python3 devtools.py base64 ""
# Error: Text cannot be empty

# Invalid JSON
python3 devtools.py json "invalid"  
# Error: Invalid JSON: Expecting value: line 1 column 1 (char 0)
```

EOF

echo "📊 Documentation build complete!"
echo ""
echo "📁 Generated Documentation:"
echo "  - README.md (Main project documentation)"
echo "  - python-tools/README.md (Python tools specific)"
echo "  - docs/USER_GUIDE.md (Complete user guide)"
echo "  - docs/DEVELOPER_GUIDE.md (Plugin development)"
echo "  - docs/EXAMPLES.md (Code examples)"
echo "  - docs/CLI_USAGE.md (Command-line usage)"
echo "  - docs/api/ (Sphinx HTML documentation)"
echo ""
echo "🌐 To view Sphinx docs: open docs/api/index.html"
echo "🚀 Documentation is ready for deployment!"