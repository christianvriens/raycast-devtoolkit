/**
 * JSON Plugin
 * Provides JSON formatting and validation functionality
 */

import { Icon, Form } from "@raycast/api";
import { PluginDefinition } from "../types";
import { BaseForm, useFormTool } from "../base";
import { PythonTools } from "../../python-tools";

// JSON Formatter Component
function JsonFormatter() {
  const { result, isLoading, handleSubmit } = useFormTool<{
    text: string;
    operation: string;
  }>();

  const format = handleSubmit(
    async (values) => {
      const jsonResult = await PythonTools.formatJson(values.text, values.operation === "minify");
      if (!jsonResult.valid) {
        throw new Error(jsonResult.error || "Invalid JSON");
      }
      return jsonResult;
    },
    {
      extractResult: (data) => data.output || "",
      getSuccessMessage: (values) => 
        `${values.operation === "minify" ? "Minified" : "Formatted"} JSON copied`,
    }
  );

  return (
    <BaseForm
      title="JSON Formatter"
      onSubmit={format}
      isLoading={isLoading}
      result={result}
      submitButtonTitle="Format JSON"
      copyButtonTitle="Copy Result"
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
    </BaseForm>
  );
}

// Plugin Definition
export const JsonPlugin: PluginDefinition = {
  id: "json-plugin",
  name: "JSON Tools",
  description: "Format, validate, and minify JSON data",
  version: "1.0.0",
  author: "DevToolkit",
  categories: [
    {
      name: "Text & Data",
      icon: Icon.Text,
      key: "text",
    },
  ],
  tools: [
    {
      name: "JSON Formatter",
      key: "json",
      icon: Icon.Document,
      categoryKey: "text",
      description: "Format, validate, and minify JSON strings",
      keywords: ["json", "format", "minify", "validate", "pretty", "parse"],
      component: JsonFormatter,
      pythonCommand: "json",
      autoCopy: true,
    },
  ],
};