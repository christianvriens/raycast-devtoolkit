/**
 * URL Plugin
 * Provides URL encoding and decoding functionality
 */

import { Icon, Form, Clipboard, showToast, Toast } from "@raycast/api";
import { useState } from "react";
import { PluginDefinition } from "../types";
import { BaseForm } from "../base";
import { PythonTools, DevToolsUtils } from "../../python-tools";

// URL Converter Component
function UrlConverter() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);
  const [validationWarning, setValidationWarning] = useState<string>("");

  const convert = async (values: { text: string; operation: string }) => {
    setIsLoading(true);
    setValidationWarning("");
    
    try {
      const data = await PythonTools.urlEncode(values.text, values.operation === "decode");
      setResult(data.output);
      
      // Check validation and set warning
      if (data.is_valid_url === false) {
        setValidationWarning("⚠️ Note: The result may not be a valid URL");
      }
      
      // Auto-copy and show success
      await Clipboard.copy(data.output);
      const operation = values.operation === "decode" ? "decoded" : "encoded";
      await showToast({
        style: Toast.Style.Success,
        title: "Copied to Clipboard",
        message: `URL ${operation} result copied`,
      });
      
    } catch (error) {
      await DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <BaseForm
      title="URL Converter"
      onSubmit={convert}
      isLoading={isLoading}
      result={result}
      submitButtonTitle="Convert"
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
      {validationWarning && (
        <Form.Description
          title="Validation"
          text={validationWarning}
        />
      )}
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
export const UrlPlugin: PluginDefinition = {
  id: "url-plugin",
  name: "URL Tools",
  description: "URL encoding and decoding utilities",
  version: "1.0.0",
  author: "DevToolkit",
  categories: [
    {
      name: "Encoding & Decoding",
      icon: Icon.Code,
      key: "encoding",
    },
  ],
  tools: [
    {
      name: "URL Encode/Decode",
      key: "url",
      icon: Icon.Link,
      categoryKey: "encoding",
      description: "Encode or decode URL strings",
      keywords: ["url", "encode", "decode", "encoding", "percent"],
      component: UrlConverter,
      pythonCommand: "url",
      autoCopy: true,
    },
  ],
};