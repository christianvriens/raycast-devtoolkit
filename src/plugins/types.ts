/**
 * Plugin System Types
 * Defines the interfaces and types for the pluggable dev toolkit architecture
 */

import { Icon } from "@raycast/api";
import { ReactElement } from "react";

export interface PluginCategory {
  name: string;
  icon: Icon;
  key: string;
}

export interface PluginTool {
  name: string;
  key: string;
  icon: Icon;
  categoryKey: string;
  description?: string;
  keywords?: string[];
  component: () => ReactElement;
  pythonCommand?: string; // The Python command this tool uses (e.g., "base64", "hash")
  autoCopy?: boolean; // Whether this tool should auto-copy results
}

export interface PluginDefinition {
  id: string;
  name: string;
  description: string;
  version: string;
  author?: string;
  categories: PluginCategory[];
  tools: PluginTool[];
}

// Plugin registration interface
export interface PluginRegistry {
  registerPlugin(plugin: PluginDefinition): void;
  getCategories(): PluginCategory[];
  getToolsByCategory(categoryKey: string): PluginTool[];
  getAllTools(): PluginTool[];
  getToolByKey(key: string): PluginTool | undefined;
}

// Plugin component props
export interface PluginComponentProps {
  onResult?: (result: any) => void;
  onError?: (error: Error) => void;
}