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

