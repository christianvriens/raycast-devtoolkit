/**
 * Hash Plugin
 * Provides hash generation functionality for various algorithms
 */

import { Icon, Form } from "@raycast/api";
import { PluginDefinition } from "../types";
import { BaseForm, useFormTool } from "../base";
import { PythonTools } from "../../python-tools";

// Hash Generator Component
function HashGenerator() {
  const { result, isLoading, handleSubmit } = useFormTool<{
    text: string;
    algorithm: string;
  }>();

  const generate = handleSubmit(
    async (values) => {
      return await PythonTools.generateHash(values.text, values.algorithm as any);
    },
    {
      extractResult: (data) => data.hash,
      getSuccessMessage: (values) => `${values.algorithm.toUpperCase()} hash copied`,
    }
  );

  return (
    <BaseForm
      title="Hash Generator"
      onSubmit={generate}
      isLoading={isLoading}
      result={result}
      submitButtonTitle="Generate Hash"
      copyButtonTitle="Copy Hash"
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
    </BaseForm>
  );
}

// Plugin Definition
export const HashPlugin: PluginDefinition = {
  id: "hash-plugin",
  name: "Hash Tools",
  description: "Generate cryptographic hashes using various algorithms",
  version: "1.0.0",
  author: "DevToolkit",
  categories: [
    {
      name: "Security & Auth",
      icon: Icon.Key,
      key: "security",
    },
  ],
  tools: [
    {
      name: "Hash Generator",
      key: "hash",
      icon: Icon.Fingerprint,
      categoryKey: "security",
      description: "Generate MD5, SHA1, SHA256, or SHA512 hashes",
      keywords: ["hash", "md5", "sha1", "sha256", "sha512", "crypto", "checksum"],
      component: HashGenerator,
      pythonCommand: "hash",
      autoCopy: true,
    },
  ],
};