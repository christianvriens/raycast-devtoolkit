# DevToolkit User Guide

Complete guide to using all 8 developer tools in the DevToolkit extension.

## 🚀 Getting Started

1. **Install**: Add DevToolkit to Raycast from the extension store
2. **Access**: Press `⌘ Space` and type the tool name
3. **Use**: Fill in the form and press Enter
4. **Copy**: Results are automatically copied to your clipboard

### Install from local code (developer)

If you prefer to run DevToolkit from your local checkout (useful for development and testing), Raycast can load extensions from a local folder:

- Open Raycast → Preferences (⌘ ,) → Extensions (or Developer settings).
- Look for the option to add an "Application Directory" or a local extensions path.
- Add/select the path where this repository is located (for example: `/path/to/devtoolkit`).
- Restart Raycast or use Developer → Reload Extensions to pick up changes.

Once added, Raycast will load the extension code from that directory so you can test changes without publishing to the store. The Python CLI tools in `python-tools/` will work from the same folder.

## 🛠 Tool Reference

### 🔤 Base64 Encode/Decode

**Access**: `⌘ Space` → "base64"

Encode and decode Base64 strings with validation.

**Examples**:
```
Input: "hello world"
Output: "aGVsbG8gd29ybGQ="

Input: "aGVsbG8gd29ybGQ=" (with decode option)
Output: "hello world"
```

**Features**:
- ✅ Automatic operation detection
- ✅ Unicode text support
- ✅ Invalid Base64 detection
- ✅ Auto-copy result

**Use Cases**:
- API authentication tokens
- Email attachment encoding
- Data transmission encoding
- Configuration file encoding

---

### 🔗 URL Encode/Decode

**Access**: `⌘ Space` → "url"

Encode and decode URL strings with validation warnings.

**Examples**:
```
Input: "hello world"
Output: "hello%20world"

Input: "user@example.com"
Output: "user%40example.com"

Input: "hello%20world" (with decode option)
Output: "hello world"
```

**Features**:
- ✅ Percent encoding/decoding
- ✅ Special character handling
- ⚠️ URL validation warnings
- ✅ Auto-copy result

**Use Cases**:
- Query parameter encoding
- Form data encoding  
- URL path component encoding
- API endpoint construction

---

### 🔐 Hash Generator

**Access**: `⌘ Space` → "hash"

Generate cryptographic hashes using multiple algorithms.

**Supported Algorithms**:
- **MD5**: Fast, 32-character hash (legacy use)
- **SHA1**: 40-character hash (legacy use)
- **SHA256**: 64-character hash (recommended)
- **SHA512**: 128-character hash (high security)

**Examples**:
```
Input: "hello" (SHA256)
Output: "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

Input: "secret" (MD5)
Output: "5ebe2294ecd0e0f08eab7690d2a6ee69"
```

**Features**:
- ✅ Multiple hash algorithms
- ✅ Large text support
- ✅ Unicode text handling
- ✅ Hash length display

**Use Cases**:
- Password verification
- File integrity checking
- Data fingerprinting
- Checksums and validation

---

### 🎫 JWT Decoder

**Access**: `⌘ Space` → "jwt"

Decode and analyze JSON Web Tokens with expiration checking.

**Example**:
```
Input: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

Output:
- Header: {"alg": "HS256", "typ": "JWT"}
- Payload: {"sub": "1234567890", "name": "John Doe", ...}
- Expiration: Valid/Expired status
- Timestamps: Human-readable dates
```

**Features**:
- ✅ Complete JWT decoding
- ✅ Expiration analysis
- ✅ Human-readable timestamps
- ✅ Token validation
- ⚠️ Invalid token handling

**Use Cases**:
- Authentication debugging
- API token analysis
- Security audit
- Token expiration checking

---

### 📄 JSON Formatter

**Access**: `⌘ Space` → "json"

Format, validate, and minify JSON strings with size comparison.

**Examples**:
```
Format:
Input: '{"name":"John","age":30}'
Output: 
{
  "age": 30,
  "name": "John"
}

Minify:
Input: '{\n  "name": "John",\n  "age": 30\n}'
Output: '{"age":30,"name":"John"}'
```

**Features**:
- ✅ Pretty formatting
- ✅ JSON minification
- ✅ Syntax validation
- ✅ Size comparison
- ✅ Unicode support

**Use Cases**:
- API response formatting
- Configuration file cleanup
- JSON debugging
- Data transmission optimization

---

### 🆔 UUID Generator

**Access**: `⌘ Space` → "uuid"

Generate UUID v1 or v4 identifiers with batch support.

**UUID Versions**:
- **v1**: Time-based UUID (includes timestamp and MAC address)
- **v4**: Random UUID (recommended for most uses)

**Examples**:
```
Single UUID v4:
Output: "550e8400-e29b-41d4-a716-446655440000"

Multiple UUIDs (count: 3):
Output: 
- "6ba7b810-9dad-11d1-80b4-00c04fd430c8"
- "6ba7b811-9dad-11d1-80b4-00c04fd430c8"  
- "6ba7b812-9dad-11d1-80b4-00c04fd430c8"
```

**Features**:
- ✅ UUID v1 and v4 generation
- ✅ Batch generation (up to 100)
- ✅ Format validation
- ✅ Unique identifier guarantee

**Use Cases**:
- Database primary keys
- Unique identifiers
- Session tokens
- Correlation IDs

---

### ⏰ Epoch Converter

**Access**: `⌘ Space` → "epoch"

Convert Unix timestamps to human-readable formats with timezone support.

**Examples**:
```
Current time (empty input):
Output: 
- Epoch: 1640995200
- UTC: "2022-01-01 00:00:00 UTC"
- Local: "2022-01-01 01:00:00 CET"
- Relative: "5 minutes ago"

Specific timestamp (1640995200):
Output:
- Epoch: 1640995200
- UTC: "2022-01-01 00:00:00 UTC"
- Formats: ISO, readable, dd/mm/yyyy
```

**Features**:
- ✅ Current time conversion
- ✅ Specific timestamp conversion
- ✅ Millisecond support
- ✅ Multiple time formats
- ✅ Relative time display
- ✅ Timezone handling

**Use Cases**:
- Log file analysis
- Database timestamp debugging
- API response analysis
- Time calculation

---

### 🎨 Color Converter

**Access**: `⌘ Space` → "color"

Convert between color formats: HEX, RGB, HSL with CSS output.

**Supported Formats**:
- **HEX**: #FF0000, #f00, FF0000
- **RGB**: rgb(255, 0, 0)
- **HSL**: hsl(0, 100%, 50%)

**Examples**:
```
Input: "#ff0000"
Output:
- HEX: "#ff0000"
- RGB: {r: 255, g: 0, b: 0}
- HSL: {h: 0, s: 100, l: 50}
- CSS RGB: "rgb(255, 0, 0)"
- CSS HSL: "hsl(0, 100%, 50%)"

Input: "rgb(128, 128, 128)"
Output:
- HEX: "#808080"
- RGB: {r: 128, g: 128, b: 128}
- HSL: {h: 0, s: 0, l: 50}
```

**Features**:
- ✅ Multi-format input
- ✅ Complete format conversion
- ✅ CSS-ready output
- ✅ Color validation
- ✅ Short hex support

**Use Cases**:
- Web development
- Design system work
- CSS color conversion
- Color palette creation

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|---------|
| `⌘ + Enter` | Submit form |
| `⌘ + C` | Copy result |
| `⌘ + W` | Close extension |
| `Tab` | Navigate form fields |
| `Shift + Tab` | Navigate backwards |

## 💡 Pro Tips

### General Usage
- **Auto-Copy**: All tools automatically copy results to clipboard
- **Form Memory**: Recent inputs are remembered between uses
- **Error Handling**: Clear error messages with actionable suggestions
- **Unicode Support**: All tools handle international characters

### Workflow Tips
- **Chain Operations**: Copy output from one tool as input to another
- **Batch Processing**: Use UUID generator for multiple IDs at once
- **Quick Access**: Create custom shortcuts for frequently used tools
- **Validation**: Tools provide feedback on input validity

### Integration
- **CLI Access**: All tools available as standalone Python scripts
- **API Integration**: JSON output suitable for automation
- **Development**: Perfect for debugging API responses and tokens

## 🔧 Troubleshooting

### Common Issues

**"Invalid input" errors**:
- Check input format matches expected pattern
- Remove extra whitespace or hidden characters
- Verify special characters are properly encoded

**Base64 decode failures**:
- Ensure input is valid Base64 (use validation)
- Check for missing padding (=) characters
- Verify no line breaks in long tokens

**JWT decode issues**:
- Verify token has three parts separated by dots
- Check token hasn't been truncated
- Ensure Base64URL encoding is intact

**JSON formatting errors**:
- Validate JSON syntax before formatting
- Check for trailing commas
- Verify proper quote usage

**Color conversion problems**:
- Ensure HEX colors include # prefix or are 6 characters
- Check RGB values are between 0-255
- Verify HSL percentages are correct

### Getting Help

1. **Check input format**: Most errors are input-related
2. **Try examples**: Use examples from this guide
3. **Clear and retry**: Reset form and try again
4. **Check console**: Development console may show additional details

## 📚 Advanced Usage

### Automation

You can use the Python tools directly for automation:

```bash
# Batch encode multiple strings
for text in "hello" "world" "test"; do
  python3 python-tools/devtools.py base64 "$text"
done

# Process JWT tokens from file
cat tokens.txt | while read token; do
  python3 python-tools/devtools.py jwt "$token"
done
```

### Integration Examples

```javascript
// Node.js integration
const { exec } = require('child_process');

function encodeBase64(text) {
  return new Promise((resolve, reject) => {
    exec(`python3 devtools.py base64 "${text}"`, (error, stdout) => {
      if (error) reject(error);
      else resolve(JSON.parse(stdout));
    });
  });
}
```

---

**DevToolkit: Your swiss army knife for developer utilities! 🛠️**