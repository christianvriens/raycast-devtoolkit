/**
 * UUID Plugin
 * Provides UUID generation functionality
 */

import { Icon, Form } from "@raycast/api";
import { PluginDefinition } from "../types";
import { BaseForm, useFormTool } from "../base";
import { PythonTools } from "../../python-tools";

// UUID Generator Component
function UuidGenerator() {
  const { result, isLoading, handleSubmit } = useFormTool<{
    version: string;
    count: string;
  }>();

  const generate = handleSubmit(
    async (values) => {
      return await PythonTools.generateUuid(
        parseInt(values.version) as 1 | 4,
        parseInt(values.count)
      );
    },
    {
      extractResult: (data) => data.uuids.join('\n'),
      getSuccessMessage: (values) => {
        const count = parseInt(values.count);
        return `${count} UUID${count > 1 ? 's' : ''} copied`;
      },
    }
  );

  return (
    <BaseForm
      title="UUID Generator"
      onSubmit={generate}
      isLoading={isLoading}
      result={result}
      submitButtonTitle="Generate UUIDs"
      copyButtonTitle="Copy UUIDs"
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
          defaultValue={result}
        />
      )}
    </BaseForm>
  );
}

// Plugin Definition
export const UuidPlugin: PluginDefinition = {
  id: "uuid-plugin",
  name: "UUID Tools",
  description: "Generate unique identifiers (UUIDs)",
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
      name: "UUID Generator",
      key: "uuid",
      icon: Icon.Hashtag,
      categoryKey: "text",
      description: "Generate Version 1 or Version 4 UUIDs",
      keywords: ["uuid", "guid", "identifier", "unique", "random"],
      component: UuidGenerator,
      pythonCommand: "uuid",
      autoCopy: true,
    },
  ],
};