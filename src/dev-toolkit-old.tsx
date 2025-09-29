import { 
  ActionPanel, 
  Detail, 
  List, 
  Action, 
  Icon, 
  Form,
  showToast,
  Toast,
  Clipboard,
  useNavigation,
  LaunchProps,
} from "@raycast/api";
import { useState, useEffect } from "react";
import { PythonTools, DevToolsUtils, PythonToolsError } from "./python-tools";
import { registerAllPlugins, PluginRegistry } from "./plugins";

// Initialize plugins on module load
registerAllPlugins();

export default function Command() {
  const { push } = useNavigation();
  const categories = PluginRegistry.getCategories();

  return (
    <List searchBarPlaceholder="Search developer tools...">
      {categories.map((category) => {
        const tools = PluginRegistry.getToolsByCategory(category.key);
        
        return (
          <List.Section key={category.key} title={category.name}>
            {tools.map((tool) => (
              <List.Item
                key={tool.key}
                icon={tool.icon}
                title={tool.name}
                subtitle={tool.description}
                keywords={tool.keywords}
                actions={
                  <ActionPanel>
                    <Action
                      title="Open Tool"
                      onAction={() => push(<tool.component />)}
                    />
                  </ActionPanel>
                }
              />
            ))}
          </List.Section>
        );
      })}
    </List>
  );
}

// Legacy Tool Components (to be migrated to plugins)
function EpochConverter() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const convertEpoch = async (values: { timestamp: string }) => {
    setIsLoading(true);
    try {
      const epochResult = await PythonTools.convertEpoch(values.timestamp || undefined);
      const formatted = DevToolsUtils.formatTimestamp(epochResult);
      setResult(formatted);
    } catch (error) {
      DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Form
      isLoading={isLoading}
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Convert" onSubmit={convertEpoch} />
          {result && (
            <Action
              title="Copy Result"
              shortcut={{ modifiers: ["cmd"], key: "c" }}
              onAction={() => DevToolsUtils.copyToClipboard(result)}
            />
          )}
        </ActionPanel>
      }
    >
      <Form.TextField
        id="timestamp"
        title="Epoch Timestamp"
        placeholder="Leave empty for current time"
      />
      {result && (
        <Form.Description title="Result" text={result} />
      )}
    </Form>
  );
}

function CurrentTimestamp() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const getCurrentTime = async () => {
      try {
        const epochResult = await PythonTools.convertEpoch();
        const formatted = `Current Epoch: ${epochResult.epoch}\n\n${DevToolsUtils.formatTimestamp(epochResult)}`;
        setResult(formatted);
        
        // Automatically copy current epoch to clipboard
        await Clipboard.copy(epochResult.epoch.toString());
        await showToast({
          style: Toast.Style.Success,
          title: "Copied to Clipboard",
          message: "Current epoch timestamp copied",
        });
      } catch (error) {
        DevToolsUtils.showError(error as Error);
      } finally {
        setIsLoading(false);
      }
    };
    getCurrentTime();
  }, []);

  const refresh = async () => {
    setIsLoading(true);
    try {
      const epochResult = await PythonTools.convertEpoch();
      const formatted = `Current Epoch: ${epochResult.epoch}\n\n${DevToolsUtils.formatTimestamp(epochResult)}`;
      setResult(formatted);
      
      // Automatically copy current epoch to clipboard
      await Clipboard.copy(epochResult.epoch.toString());
      await showToast({
        style: Toast.Style.Success,
        title: "Copied to Clipboard",
        message: "Current epoch timestamp copied",
      });
    } catch (error) {
      DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Detail
      isLoading={isLoading}
      markdown={`\`\`\`\n${result}\n\`\`\``}
      actions={
        <ActionPanel>
          <Action
            title="Copy Timestamp"
            onAction={() => DevToolsUtils.copyToClipboard(result.split('\n')[0].split(': ')[1])}
          />
          <Action
            title="Copy All"
            onAction={() => DevToolsUtils.copyToClipboard(result)}
          />
          <Action
            title="Refresh"
            shortcut={{ modifiers: ["cmd"], key: "r" }}
            onAction={refresh}
          />
        </ActionPanel>
      }
    />
  );
}

function Base64Converter() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const convert = async (values: { text: string; operation: string }) => {
    setIsLoading(true);
    try {
      const base64Result = await PythonTools.base64Convert(values.text, values.operation === "decode");
      setResult(base64Result.output);
      
      // Automatically copy result to clipboard
      await Clipboard.copy(base64Result.output);
      await showToast({
        style: Toast.Style.Success,
        title: "Copied to Clipboard",
        message: `${values.operation === "decode" ? "Decoded" : "Encoded"} result copied`,
      });
    } catch (error) {
      DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Form
      isLoading={isLoading}
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Convert" onSubmit={convert} />
          {result && (
            <Action
              title="Copy Result"
              shortcut={{ modifiers: ["cmd"], key: "c" }}
              onAction={() => DevToolsUtils.copyToClipboard(result)}
            />
          )}
        </ActionPanel>
      }
    >
      <Form.TextArea
        id="text"
        title="Text"
        placeholder="Enter text to encode/decode"
      />
      <Form.Dropdown id="operation" title="Operation" defaultValue="encode">
        <Form.Dropdown.Item value="encode" title="Encode" />
        <Form.Dropdown.Item value="decode" title="Decode" />
      </Form.Dropdown>
      {result && (
        <Form.TextArea
          id="result"
          title="Result"
          value={result}
        />
      )}
    </Form>
  );
}

function UrlConverter() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const convert = async (values: { text: string; operation: string }) => {
    setIsLoading(true);
    try {
      const urlResult = await PythonTools.urlEncode(values.text, values.operation === "decode");
      setResult(urlResult.output);
      
      // Automatically copy result to clipboard
      await Clipboard.copy(urlResult.output);
      await showToast({
        style: Toast.Style.Success,
        title: "Copied to Clipboard",
        message: `URL ${values.operation === "decode" ? "decoded" : "encoded"} result copied`,
      });
    } catch (error) {
      DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Form
      isLoading={isLoading}
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Convert" onSubmit={convert} />
          {result && (
            <Action
              title="Copy Result"
              shortcut={{ modifiers: ["cmd"], key: "c" }}
              onAction={() => DevToolsUtils.copyToClipboard(result)}
            />
          )}
        </ActionPanel>
      }
    >
      <Form.TextArea
        id="text"
        title="Text"
        placeholder="Enter text to encode/decode"
      />
      <Form.Dropdown id="operation" title="Operation" defaultValue="encode">
        <Form.Dropdown.Item value="encode" title="Encode" />
        <Form.Dropdown.Item value="decode" title="Decode" />
      </Form.Dropdown>
      {result && (
        <Form.TextArea
          id="result"
          title="Result"
          value={result}
        />
      )}
    </Form>
  );
}

function JWTDecoder() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const decode = async (values: { token: string }) => {
    setIsLoading(true);
    try {
      const jwtResult = await PythonTools.decodeJWT(values.token);
      const formatted = DevToolsUtils.formatJWTInfo(jwtResult);
      setResult(formatted);
    } catch (error) {
      DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Form
      isLoading={isLoading}
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Decode" onSubmit={decode} />
          {result && (
            <Action
              title="Copy Result"
              shortcut={{ modifiers: ["cmd"], key: "c" }}
              onAction={() => DevToolsUtils.copyToClipboard(result)}
            />
          )}
        </ActionPanel>
      }
    >
      <Form.TextArea
        id="token"
        title="JWT Token"
        placeholder="Paste JWT token here"
      />
      {result && (
        <Form.Description title="Decoded Information" text={result} />
      )}
    </Form>
  );
}

function HashGenerator() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const generate = async (values: { text: string; algorithm: string }) => {
    setIsLoading(true);
    try {
      const hashResult = await PythonTools.generateHash(values.text, values.algorithm as any);
      setResult(hashResult.hash);
      
      // Automatically copy result to clipboard
      await Clipboard.copy(hashResult.hash);
      await showToast({
        style: Toast.Style.Success,
        title: "Copied to Clipboard",
        message: `${values.algorithm.toUpperCase()} hash copied`,
      });
    } catch (error) {
      DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Form
      isLoading={isLoading}
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Generate" onSubmit={generate} />
          {result && (
            <Action
              title="Copy Hash"
              shortcut={{ modifiers: ["cmd"], key: "c" }}
              onAction={() => DevToolsUtils.copyToClipboard(result)}
            />
          )}
        </ActionPanel>
      }
    >
      <Form.TextArea
        id="text"
        title="Text"
        placeholder="Enter text to hash"
      />
      <Form.Dropdown id="algorithm" title="Algorithm" defaultValue="sha256">
        <Form.Dropdown.Item value="md5" title="MD5" />
        <Form.Dropdown.Item value="sha1" title="SHA1" />
        <Form.Dropdown.Item value="sha256" title="SHA256" />
        <Form.Dropdown.Item value="sha512" title="SHA512" />
      </Form.Dropdown>
      {result && (
        <Form.TextField
          id="result"
          title="Hash"
          value={result}
        />
      )}
    </Form>
  );
}

function JsonFormatter() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const format = async (values: { text: string; operation: string }) => {
    setIsLoading(true);
    try {
      const jsonResult = await PythonTools.formatJson(values.text, values.operation === "minify");
      if (jsonResult.valid && jsonResult.output) {
        setResult(jsonResult.output);
        
        // Automatically copy result to clipboard
        await Clipboard.copy(jsonResult.output);
        await showToast({
          style: Toast.Style.Success,
          title: "Copied to Clipboard",
          message: `${values.operation === "minify" ? "Minified" : "Formatted"} JSON copied`,
        });
      } else {
        throw new Error(jsonResult.error || "Invalid JSON");
      }
    } catch (error) {
      DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Form
      isLoading={isLoading}
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Format" onSubmit={format} />
          {result && (
            <Action
              title="Copy Result"
              shortcut={{ modifiers: ["cmd"], key: "c" }}
              onAction={() => DevToolsUtils.copyToClipboard(result)}
            />
          )}
        </ActionPanel>
      }
    >
      <Form.TextArea
        id="text"
        title="JSON Text"
        placeholder="Paste JSON here"
      />
      <Form.Dropdown id="operation" title="Operation" defaultValue="format">
        <Form.Dropdown.Item value="format" title="Pretty Format" />
        <Form.Dropdown.Item value="minify" title="Minify" />
      </Form.Dropdown>
      {result && (
        <Form.TextArea
          id="result"
          title="Result"
          value={result}
        />
      )}
    </Form>
  );
}

function UuidGenerator() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const generate = async (values: { version: string; count: string }) => {
    setIsLoading(true);
    try {
      const uuidResult = await PythonTools.generateUuid(
        parseInt(values.version) as 1 | 4,
        parseInt(values.count)
      );
      const resultText = uuidResult.uuids.join('\n');
      setResult(resultText);
      
      // Automatically copy result to clipboard
      await Clipboard.copy(resultText);
      await showToast({
        style: Toast.Style.Success,
        title: "Copied to Clipboard",
        message: `${uuidResult.uuids.length} UUID${uuidResult.uuids.length > 1 ? 's' : ''} copied`,
      });
    } catch (error) {
      DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Form
      isLoading={isLoading}
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Generate" onSubmit={generate} />
          {result && (
            <Action
              title="Copy UUIDs"
              shortcut={{ modifiers: ["cmd"], key: "c" }}
              onAction={() => DevToolsUtils.copyToClipboard(result)}
            />
          )}
        </ActionPanel>
      }
    >
      <Form.Dropdown id="version" title="UUID Version" defaultValue="4">
        <Form.Dropdown.Item value="1" title="Version 1 (Time-based)" />
        <Form.Dropdown.Item value="4" title="Version 4 (Random)" />
      </Form.Dropdown>
      <Form.TextField
        id="count"
        title="Count"
        defaultValue="1"
        placeholder="Number of UUIDs to generate"
      />
      {result && (
        <Form.TextArea
          id="result"
          title="Generated UUIDs"
          value={result}
        />
      )}
    </Form>
  );
}

function ColorConverter() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const convert = async (values: { color: string }) => {
    setIsLoading(true);
    try {
      const colorResult = await PythonTools.convertColor(values.color);
      const formatted = `HEX: ${colorResult.hex}\nRGB: ${colorResult.rgb}\nHSL: ${colorResult.hsl}`;
      setResult(formatted);
    } catch (error) {
      DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Form
      isLoading={isLoading}
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Convert" onSubmit={convert} />
          {result && (
            <Action
              title="Copy Result"
              shortcut={{ modifiers: ["cmd"], key: "c" }}
              onAction={() => DevToolsUtils.copyToClipboard(result)}
            />
          )}
        </ActionPanel>
      }
    >
      <Form.TextField
        id="color"
        title="Color"
        placeholder="Enter color (e.g., #FF5733 or rgb(255, 87, 51))"
      />
      {result && (
        <Form.Description title="Converted Formats" text={result} />
      )}
    </Form>
  );
}
