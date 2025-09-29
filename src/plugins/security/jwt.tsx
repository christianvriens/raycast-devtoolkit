/**
 * JWT Plugin
 * Provides JWT token decoding functionality
 */

import { Icon, Form } from "@raycast/api";
import { PluginDefinition } from "../types";
import { BaseForm, useFormTool } from "../base";
import { PythonTools, DevToolsUtils } from "../../python-tools";

// JWT Decoder Component
function JWTDecoder() {
  const { result, isLoading, handleSubmit } = useFormTool<{
    token: string;
  }>();

  const decode = handleSubmit(
    async (values) => {
      return await PythonTools.decodeJWT(values.token);
    },
    {
      extractResult: (data) => DevToolsUtils.formatJWTInfo(data),
      getSuccessMessage: () => "JWT decoded information copied",
      autoCopy: false, // JWT info is usually too long for auto-copy
    }
  );

  return (
    <BaseForm
      title="JWT Decoder"
      onSubmit={decode}
      isLoading={isLoading}
      result={result}
      submitButtonTitle="Decode"
      copyButtonTitle="Copy JWT Info"
    >
      <Form.TextArea
        id="token"
        title="JWT Token"
        placeholder="Paste JWT token here"
      />
      {result && (
        <Form.Description title="Decoded Information" text={result} />
      )}
    </BaseForm>
  );
}

// Plugin Definition
export const JWTPlugin: PluginDefinition = {
  id: "jwt-plugin",
  name: "JWT Tools",
  description: "JWT token decoding utilities",
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
      name: "JWT Decoder",
      key: "jwt",
      icon: Icon.Key,
      categoryKey: "security",
      description: "Decode and inspect JWT tokens",
      keywords: ["jwt", "json", "web", "token", "decode", "auth"],
      component: JWTDecoder,
      pythonCommand: "jwt",
      autoCopy: false,
    },
  ],
};