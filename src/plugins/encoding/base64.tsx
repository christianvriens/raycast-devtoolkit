/**
 * Base64 Plugin
 * Provides Base64 encoding and decoding functionality
 */

import { Icon, Form } from "@raycast/api";
import { PluginDefinition } from "../types";
import { BaseForm, useFormTool } from "../base";
import { PythonTools } from "../../python-tools";

// Base64 Converter Component
function Base64Converter() {
  const { result, isLoading, handleSubmit } = useFormTool<{
    text: string;
    operation: string;
  }>();

  const convert = handleSubmit(
    async (values) => {
      return await PythonTools.base64Convert(values.text, values.operation === "decode");
    },
    {
      extractResult: (data) => data.output,
      getSuccessMessage: (values) => 
        `${values.operation === "decode" ? "Decoded" : "Encoded"} result copied`,
    }
  );

  return (
    <BaseForm
      title="Base64 Converter"
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
export const Base64Plugin: PluginDefinition = {
  id: "base64-plugin",
  name: "Base64 Tools",
  description: "Base64 encoding and decoding utilities",
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
      name: "Base64 Encode/Decode",
      key: "base64",
      icon: Icon.Document,
      categoryKey: "encoding",
      description: "Encode or decode Base64 strings",
      keywords: ["base64", "encode", "decode", "encoding"],
      component: Base64Converter,
      pythonCommand: "base64",
      autoCopy: true,
    },
  ],
};