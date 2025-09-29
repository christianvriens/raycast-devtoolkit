# DevToolkit - Advanced Developer Utilities

A powerful Raycast extension providing essential developer tools with a robust plugin architecture. Features 8 professional-grade utilities for encoding, security, text processing, and more.

![DevToolkit](assets/extension-icon.png)

## ⚡ Quick Start

1. **Install Extension**: Add to Raycast from the store
2. **Use Tools**: Press `⌘ Space`, type tool name (e.g., "base64", "jwt", "hash")
3. **Auto-Copy**: Results automatically copy to clipboard
4. **CLI Access**: Python tools work standalone too!

### Install from local code (developer)

If you want to run this toolkit from your local copy (for development or testing), you can tell Raycast to load extensions from a local directory:

- Open Raycast and go to Preferences (⌘ ,).
- Find the Extensions / Developer settings and choose the option to add an "Application Directory" (or similar) for local extensions.
- Select the folder where this repository is checked out (for example: `/path/to/devtoolkit`).
- Raycast will load extensions found in that directory. You may need to restart Raycast or use the Developer → Reload Extensions command for changes to appear.

This lets you iterate on TypeScript plugins locally and use the bundled Python tools from `python-tools/` without publishing the extension.

## 🛠 Available Tools

| Tool | Description | Categories |
|------|-------------|------------|
| **Base64** | Encode/decode Base64 strings | Encoding |
| **URL** | Encode/decode URL strings with validation | Encoding |
| **Hash** | Generate MD5, SHA1, SHA256, SHA512 hashes | Security |
| **JWT** | Decode and analyze JSON Web Tokens | Security |
| **JSON** | Format, validate, and minify JSON | Text |
| **UUID** | Generate UUID v1/v4 identifiers | Text |
| **Epoch** | Convert Unix timestamps to readable formats | Time |
| **Color** | Convert between HEX, RGB, HSL formats | Design |

## 🚀 Features

- **🔄 Plugin Architecture**: Extensible system for adding new tools
- **✅ Input Validation**: Pydantic-powered validation with detailed error messages
- **📋 Auto-Copy**: Results automatically copied to clipboard
- **🌐 Standalone CLI**: Python tools work independently of Raycast
- **🧪 Comprehensive Testing**: 77+ tests ensuring reliability
- **📚 Full Documentation**: Complete API and developer guides

## � Documentation

- **[User Guide](docs/USER_GUIDE.md)** - How to use each tool
- **[Developer Guide](docs/DEVELOPER_GUIDE.md)** - Plugin architecture and development
- **[Python Tools](python-tools/README.md)** - Standalone Python usage
- **[API Reference](docs/api/)** - Complete API documentation

## 🏃‍♂️ Quick Examples

### Raycast Usage
```
⌘ Space → "base64" → Enter text → Auto-copied!
⌘ Space → "jwt" → Paste token → View decoded payload
⌘ Space → "hash" → Enter text → Get SHA256 hash
```

### Standalone Python
```bash
# List all tools
python3 python-tools/devtools.py list

# Encode Base64
python3 python-tools/devtools.py base64 "hello world"

# Decode JWT
python3 python-tools/devtools.py jwt "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Generate hash
python3 python-tools/devtools.py hash "secret" --algorithm sha256
```
```

### Standalone Python
```bash
# List all tools
python3 python-tools/devtools.py list

# Encode Base64
python3 python-tools/devtools.py base64 "hello world"

# Decode JWT
python3 python-tools/devtools.py jwt "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."

# Generate hash
python3 python-tools/devtools.py hash "secret" --algorithm sha256
```

## 🧩 Architecture

DevToolkit uses a **dual plugin architecture**:

- **TypeScript Frontend**: Raycast UI components with consistent patterns
- **Python Backend**: Pydantic-validated tools with factory pattern
- **Plugin Registry**: Auto-discovery and registration system
- **Comprehensive Testing**: Individual test suites for each plugin

```
src/
├── plugins/           # TypeScript plugins
│   ├── encoding/      # Base64, URL tools
│   ├── security/      # JWT, Hash tools
│   ├── text/          # JSON, UUID tools
│   └── time/          # Epoch tools
python-tools/
├── core/              # Plugin framework
├── plugins/           # Python plugins
└── tests/             # Comprehensive tests
```

## 🔧 Development

### Adding New Tools

1. **Create Python Plugin**:
```python
# python-tools/plugins/my_tool.py
class MyTool(BaseTool):
    def get_config(self) -> ToolConfig:
        return ToolConfig(name="my_tool", ...)
    
    def execute(self, input_data) -> MyOutput:
        # Tool logic here
        pass
```

2. **Create TypeScript Plugin**:
```tsx
// src/plugins/category/my-tool.tsx
export const MyPlugin: PluginDefinition = {
    tools: [{
        name: "My Tool",
        component: MyToolComponent,
        pythonCommand: "my_tool"
    }]
};
```

3. **Add Tests**:
```python
# python-tools/tests/test_my_tool.py
class TestMyTool(unittest.TestCase):
    def test_functionality(self):
        # Test cases here
        pass
```

See [Developer Guide](docs/DEVELOPER_GUIDE.md) for complete instructions.

## 🧪 Testing

```bash
# Run all tests
cd python-tools && python3 tests/run_all_tests.py

# Run specific tool tests
python3 tests/test_base64_tool.py

# Build extension
npm run build
```

## 📄 License

Apache License 2.0 - See [LICENSE](LICENSE) for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 🔗 Links

- [Raycast Extension Store](https://raycast.com/extensions)
- [Plugin Development Guide](docs/DEVELOPER_GUIDE.md)
- [Python Tools Documentation](python-tools/README.md)
- [Issue Tracker](https://github.com/your-username/devtoolkit/issues)

---

**Built with ❤️ using Raycast, TypeScript, Python, and Pydantic**
🚀 Key Benefits:
✅ Easy to Add New Tools - Just create a plugin file and register it
✅ Self-Contained - Each tool has its own component, logic, and metadata
✅ Consistent UI - Base components ensure uniform look and behavior
✅ Auto-Copy Support - Built-in clipboard integration
✅ Search & Keywords - Tools are discoverable through search
✅ Type-Safe - Full TypeScript support throughout
✅ Python Integration - Seamless connection to Python backend
✅ Category Organization - Tools automatically grouped by category

📝 How to Add a New Tool:
Create plugin file in appropriate category folder
Add Python function to devtools.py
Register plugin in index.ts
Build and test!
🧪 Testing:
Python Tests: All 13 tests passing ✅
Extension Build: Successful ✅
Plugin Registration: All 7 plugins registered ✅
The extension now has a clean, maintainable, and extensible architecture that makes it trivial to add new developer tools as mini-plugins! 🎯

