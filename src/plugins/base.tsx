/**
 * Base Plugin Components
 * Reusable components and utilities for building dev tool plugins
 */

import { 
  ActionPanel, 
  Form, 
  Action, 
  showToast,
  Toast,
  Clipboard,
} from "@raycast/api";
import { useState } from "react";
import { PythonTools, DevToolsUtils } from "../python-tools";

export interface BaseFormProps {
  title: string;
  onSubmit: (values: any) => Promise<void>;
  isLoading?: boolean;
  children: React.ReactNode;
  result?: string;
  copyButtonTitle?: string;
  submitButtonTitle?: string;
}

/**
 * Base form component that handles common form patterns
 */
export function BaseForm({ 
  title, 
  onSubmit, 
  isLoading = false, 
  children, 
  result, 
  copyButtonTitle = "Copy Result",
  submitButtonTitle = "Submit"
}: BaseFormProps) {
  return (
    <Form
      isLoading={isLoading}
      actions={
        <ActionPanel>
          <Action.SubmitForm title={submitButtonTitle} onSubmit={onSubmit} />
          {result && (
            <Action
              title={copyButtonTitle}
              shortcut={{ modifiers: ["cmd"], key: "c" }}
              onAction={() => DevToolsUtils.copyToClipboard(result)}
            />
          )}
        </ActionPanel>
      }
    >
      {children}
    </Form>
  );
}

/**
 * Hook for handling Python tool execution with auto-copy
 */
export function usePythonTool() {
  const [result, setResult] = useState<string>("");
  const [isLoading, setIsLoading] = useState(false);

  const execute = async <T,>(
    pythonFunction: () => Promise<T>,
    options: {
      extractResult: (data: T) => string;
      successMessage: string;
      autoCopy?: boolean;
    }
  ) => {
    setIsLoading(true);
    try {
      const data = await pythonFunction();
      const extractedResult = options.extractResult(data);
      setResult(extractedResult);
      
      // Auto-copy if enabled
      if (options.autoCopy !== false) {
        await Clipboard.copy(extractedResult);
        await showToast({
          style: Toast.Style.Success,
          title: "Copied to Clipboard",
          message: options.successMessage,
        });
      }
    } catch (error) {
      DevToolsUtils.showError(error as Error);
    } finally {
      setIsLoading(false);
    }
  };

  return { result, isLoading, execute, setResult };
}

/**
 * Hook for handling form-based tools
 */
export function useFormTool<T = any>() {
  const { result, isLoading, execute, setResult } = usePythonTool();

  const handleSubmit = (
    pythonFunction: (values: T) => Promise<any>,
    options: {
      extractResult: (data: any, values: T) => string;
      getSuccessMessage: (values: T) => string;
      autoCopy?: boolean;
    }
  ) => {
    return async (values: T) => {
      await execute(
        () => pythonFunction(values),
        {
          extractResult: (data: any) => options.extractResult(data, values),
          successMessage: options.getSuccessMessage(values),
          autoCopy: options.autoCopy,
        }
      );
    };
  };

  return { result, isLoading, handleSubmit, setResult };
}