# DevToolkit Plugin System

The DevToolkit now uses a pluggable architecture that makes it easy to add new developer tools. Each tool is a self-contained mini-plugin that can be easily added, removed, or modified.

## Plugin Architecture

### 📁 File Structure

```
src/
  plugins/
    types.ts          # Plugin type definitions
    registry.ts       # Plugin registry system
    base.tsx         # Base components and hooks
    index.ts         # Plugin registration
    encoding/        # Encoding & decoding plugins
      base64.tsx
      url.tsx
    security/        # Security & authentication plugins
      jwt.tsx
      hash.tsx
    text/           # Text & data processing plugins
      uuid.tsx
      json.tsx
    time/           # Time & date plugins
      timestamp.tsx
```

## Creating a New Plugin

### 1. Create Plugin Component

Create a new file in the appropriate category folder (or create a new category):

```tsx
// src/plugins/category/your-tool.tsx
import { Icon, Form } from "@raycast/api";
import { PluginDefinition } from "../types";
import { BaseForm, useFormTool } from "../base";
import { PythonTools } from "../../python-tools";

// Your Tool Component
function YourTool() {
  const { result, isLoading, handleSubmit } = useFormTool<{
    input: string;
  }>();

  const process = handleSubmit(
    async (values) => {
      return await PythonTools.yourPythonFunction(values.input);
    },
    {
      extractResult: (data) => data.output,
      getSuccessMessage: () => "Result copied to clipboard",
    }
  );

  return (
    <BaseForm
      title="Your Tool"
      onSubmit={process}
      isLoading={isLoading}
      result={result}
      submitButtonTitle="Process"
    >
      <Form.TextField
        id="input"
        title="Input"
        placeholder="Enter your input"
      />
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
export const YourToolPlugin: PluginDefinition = {
  id: "your-tool-plugin",
  name: "Your Tool",
  description: "Description of what your tool does",
  version: "1.0.0",
  author: "Your Name",
  categories: [
    {
      name: "Your Category",
      icon: Icon.YourIcon,
      key: "your-category",
    },
  ],
  tools: [
    {
      name: "Your Tool Name",
      key: "your-tool",
      icon: Icon.YourIcon,
      categoryKey: "your-category",
      description: "Brief description",
      keywords: ["keyword1", "keyword2"],
      component: YourTool,
      pythonCommand: "your-command",
      autoCopy: true,
    },
  ],
};
```

### 2. Add Python Function

Add your Python function to `python-tools/devtools.py`:

```python
@staticmethod
def your_python_function(input_text: str) -> Dict[str, Any]:
    """Your function description."""
    # Your Python logic here
    result = process_input(input_text)
    
    return {
        "input": input_text,
        "output": result,
        "operation": "your-operation"
    }
```

### 3. Add CLI Command

Add CLI support in the `main()` function:

```python
# In main() function
your_parser = subparsers.add_parser('your-command', help='Your command help')
your_parser.add_argument('input', help='Input to process')

# In the try block
elif args.command == 'your-command':
    result = DevTools.your_python_function(args.input)
```

### 4. Register Plugin

Add your plugin to `src/plugins/index.ts`:

```tsx
import { YourToolPlugin } from "./category/your-tool";

export function registerAllPlugins() {
  // ... existing registrations
  PluginRegistry.registerPlugin(YourToolPlugin);
}
```

### 5. Add TypeScript Interface (if needed)

If your Python function returns complex data, add the interface to `src/python-tools.ts`:

```tsx
export interface YourToolResult {
  input: string;
  output: string;
  operation: string;
}

// In PythonTools class
static async yourPythonFunction(input: string): Promise<YourToolResult> {
  return executePythonTool("your-command", [input]);
}
```

## Plugin Features

### 🔧 Built-in Hooks

- **`useFormTool<T>()`** - Handle form-based tools with auto-copy
- **`usePythonTool()`** - Execute Python tools with loading states
- **`BaseForm`** - Pre-styled form component with actions

### 🎯 Auto-Copy Support

Set `autoCopy: true` in your tool definition to automatically copy results to clipboard.

### 🔍 Search & Keywords

Add relevant keywords to make your tool discoverable through search.

### 🏷️ Categories

Tools are automatically grouped by category. If multiple plugins use the same category key, they'll be merged under one section.

## Example Plugins

Look at existing plugins for reference:

- **Simple Tools**: `base64.tsx`, `url.tsx`, `hash.tsx`
- **Complex UI**: `timestamp.tsx` (multiple components)
- **Custom Logic**: `jwt.tsx` (no auto-copy)

## Benefits of Plugin System

✅ **Modular** - Each tool is self-contained  
✅ **Reusable** - Common patterns abstracted into base components  
✅ **Discoverable** - Automatic registration and categorization  
✅ **Maintainable** - Clear separation of concerns  
✅ **Extensible** - Easy to add new tools without touching existing code  
✅ **Type-Safe** - Full TypeScript support  
✅ **Consistent** - Standardized UI and behavior patterns  

## Testing

After adding a plugin:

1. Build: `npm run build`
2. Test in Raycast
3. Verify Python function: `python3 python-tools/devtools.py your-command "test"`
4. Run tests: `python3 python-tools/test_devtools_new.py`

## 🎯 Recommended Workflow

### Current Development Flow:
```bash
# 1. Develop in python-tools/
vim python-tools/plugins/new_tool.py

# 2. Test in development
python3 python-tools/tests/test_new_tool.py

# 3. Copy to assets for Raycast
cp -r python-tools/* assets/

# 4. Build extension
npm run build
```

### 💡 Alternative Approaches:

You could potentially simplify this workflow by:

- **Use symlinks**: `ln -s python-tools/* assets/`
- **Use build scripts** to auto-copy during development
- **Configure Raycast** to use python-tools directly

However, the current setup gives you:
- ✅ **Clear separation** between development and distribution
- ✅ **Version control** over what gets packaged
- ✅ **Flexibility** to customize the assets folder independently
- ✅ **Safety** - no accidental changes to development code

## Development Tips

### Project Structure Understanding
```
devtoolkit/
├── python-tools/          # 🛠️ Development environment
│   ├── core/             # Plugin system core
│   ├── plugins/          # Individual tool plugins  
│   ├── tests/            # Comprehensive test suite
│   └── devtools.py       # CLI interface
├── assets/               # 📦 Raycast distribution copy
│   └── (mirrors python-tools structure)
└── src/                  # 🎨 TypeScript/Raycast UI
    └── plugins/          # UI plugin system
```

### Best Practices
- **Develop in `python-tools/`** - This is your main development environment
- **Test thoroughly** before copying to `assets/`
- **Use the plugin registry** for consistent tool discovery
- **Follow naming conventions** for predictable behavior
- **Document your plugins** with clear descriptions and examples

Happy plugin development! 🚀