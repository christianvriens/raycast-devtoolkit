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

