/**
 * Escape/Unescape Plugin
 * Provides UI for escaping and unescaping HTML, JSON, XML, and JavaScript strings
 */

import { Icon, Form } from "@raycast/api";
import { PluginDefinition } from "../types";
import { BaseForm, useFormTool } from "../base";
import { PythonTools } from "../../python-tools";

function EscapeForm() {
  const { result, isLoading, handleSubmit } = useFormTool<{ text: string; operation: string; format: string }>();

  const realSubmit = handleSubmit(
    async (values) => {
      const out = await PythonTools.escapeText(values.text, values.operation as any, values.format);
      return out;
    },
    {
      extractResult: (data) => (data && (data as any).output_text) || "",
      getSuccessMessage: (values) => `${values.operation === "escape" ? "Escaped" : "Unescaped"} (${values.format}) copied`,
    }
  );
  return (
    <BaseForm
      title="Escape / Unescape"
      onSubmit={realSubmit}
      isLoading={isLoading}
      result={result}
      submitButtonTitle="Run"
      copyButtonTitle="Copy Result"
    >
      <Form.TextArea id="text" title="Text" placeholder="Paste text to escape or unescape" />
      <Form.Dropdown id="operation" title="Operation" defaultValue="escape">
        <Form.Dropdown.Item value="escape" title="Escape" />
        <Form.Dropdown.Item value="unescape" title="Unescape" />
      </Form.Dropdown>
      <Form.Dropdown id="format" title="Format" defaultValue="html">
        <Form.Dropdown.Item value="html" title="HTML" />
        <Form.Dropdown.Item value="json" title="JSON" />
        <Form.Dropdown.Item value="xml" title="XML" />
        <Form.Dropdown.Item value="javascript" title="JavaScript" />
      </Form.Dropdown>
  {result && <Form.TextArea id="result" title="Result" defaultValue={result} />}
    </BaseForm>
  );
}

// Small wrapper to call PythonTools (keeps TS code tidy)
const PythonToolsInstance = {
  async runEscape(text: string, operation: string, format: string) {
    // We call the python 'escape' command; pass args as JSON via stdin for safety
    return (await (PythonTools as any).execute ? (PythonTools as any).execute('escape', [JSON.stringify({ text, operation, format })]) : PythonTools.formatJson(text)) as any;
  },
};

export const EscapePlugin: PluginDefinition = {
  id: "escape-plugin",
  name: "Escape / Unescape",
  description: "Escape or unescape HTML, JSON, XML and JavaScript strings",
  version: "1.0.0",
  author: "DevToolkit",
  categories: [
    {
      name: "Escape / Unescape",
      icon: Icon.TextCursor,
      key: "escape",
    },
  ],
  tools: [
    {
      name: "Escape / Unescape",
      key: "escape",
      icon: Icon.TextCursor,
      categoryKey: "escape",
      description: "Escape or unescape text for HTML/JSON/XML/JS",
      keywords: ["escape", "unescape", "html", "json", "xml", "javascript", "escaping"],
      component: EscapeForm,
      pythonCommand: "escape",
      autoCopy: true,
    },
  ],
};
