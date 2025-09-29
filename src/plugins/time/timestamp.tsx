/**
 * Timestamp Plugin
 * Provides epoch timestamp conversion and current time utilities
 */

import { Icon, Form, Detail, ActionPanel, Action, Clipboard, showToast, Toast, useNavigation } from "@raycast/api";
import { useState, useEffect } from "react";
import { PluginDefinition } from "../types";
import { BaseForm, useFormTool, usePythonTool } from "../base";
import { PythonTools, DevToolsUtils } from "../../python-tools";

// Epoch Converter Component
function EpochConverter() {
  const { result, isLoading, handleSubmit } = useFormTool<{
    timestamp: string;
  }>();

  const convert = handleSubmit(
    async (values) => {
      return await PythonTools.convertEpoch(values.timestamp || undefined);
    },
    {
      extractResult: (data) => DevToolsUtils.formatTimestamp(data),
      getSuccessMessage: () => "Timestamp conversion copied",
      autoCopy: false, // Too much text for auto-copy
    }
  );

  return (
    <BaseForm
      title="Epoch Converter"
      onSubmit={convert}
      isLoading={isLoading}
      result={result}
      submitButtonTitle="Convert"
      copyButtonTitle="Copy Result"
    >
      <Form.TextField
        id="timestamp"
        title="Epoch Timestamp"
        placeholder="Leave empty for current time"
      />
      {result && (
        <Form.Description title="Result" text={result} />
      )}
    </BaseForm>
  );
}

// Current Timestamp Component
function CurrentTimestamp() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);

  const getCurrentTime = async () => {
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

  useEffect(() => {
    getCurrentTime();
  }, []);

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
            onAction={getCurrentTime}
          />
        </ActionPanel>
      }
    />
  );
}

// Plugin Definition
export const TimestampPlugin: PluginDefinition = {
  id: "timestamp-plugin",
  name: "Timestamp Tools",
  description: "Work with epoch timestamps and current time",
  version: "1.0.0",
  author: "DevToolkit",
  categories: [
    {
      name: "Time & Date",
      icon: Icon.Clock,
      key: "time",
    },
  ],
  tools: [
    {
      name: "Epoch Converter",
      key: "epoch",
      icon: Icon.Calendar,
      categoryKey: "time",
      description: "Convert epoch timestamps to human-readable formats",
      keywords: ["epoch", "timestamp", "unix", "time", "date", "convert"],
      component: EpochConverter,
      pythonCommand: "epoch",
      autoCopy: false,
    },
    {
      name: "Current Timestamp",
      key: "current-epoch",
      icon: Icon.Clock,
      categoryKey: "time",
      description: "Get current epoch timestamp",
      keywords: ["current", "now", "timestamp", "epoch", "time"],
      component: CurrentTimestamp,
      pythonCommand: "epoch",
      autoCopy: true,
    },
  ],
};