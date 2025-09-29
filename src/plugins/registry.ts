/**
 * Plugin Registry
 * Centralized system for registering and managing dev tool plugins
 */

import { PluginDefinition, PluginCategory, PluginTool, PluginRegistry as IPluginRegistry } from './types';

class PluginRegistryImpl implements IPluginRegistry {
  private plugins: Map<string, PluginDefinition> = new Map();
  private categories: Map<string, PluginCategory> = new Map();
  private tools: Map<string, PluginTool> = new Map();

  registerPlugin(plugin: PluginDefinition): void {
    if (this.plugins.has(plugin.id)) {
      throw new Error(`Plugin with id '${plugin.id}' is already registered`);
    }

    // Register the plugin
    this.plugins.set(plugin.id, plugin);

    // Register categories (merge if category already exists, keep first icon)
    plugin.categories.forEach(category => {
      if (!this.categories.has(category.key)) {
        this.categories.set(category.key, category);
      }
    });

    // Register tools
    plugin.tools.forEach(tool => {
      if (this.tools.has(tool.key)) {
        throw new Error(`Tool with key '${tool.key}' is already registered`);
      }
      
      // Validate that the tool's category exists
      if (!this.categories.has(tool.categoryKey)) {
        throw new Error(`Tool '${tool.key}' references unknown category '${tool.categoryKey}'`);
      }
      
      this.tools.set(tool.key, tool);
    });

    console.log(`Registered plugin: ${plugin.name} (${plugin.tools.length} tools)`);
  }

  getCategories(): PluginCategory[] {
    return Array.from(this.categories.values()).sort((a, b) => a.name.localeCompare(b.name));
  }

  getToolsByCategory(categoryKey: string): PluginTool[] {
    return Array.from(this.tools.values())
      .filter(tool => tool.categoryKey === categoryKey)
      .sort((a, b) => a.name.localeCompare(b.name));
  }

  getAllTools(): PluginTool[] {
    return Array.from(this.tools.values()).sort((a, b) => a.name.localeCompare(b.name));
  }

  getToolByKey(key: string): PluginTool | undefined {
    return this.tools.get(key);
  }

  // Debug methods
  listPlugins(): string[] {
    return Array.from(this.plugins.keys());
  }

  getPluginInfo(id: string): PluginDefinition | undefined {
    return this.plugins.get(id);
  }
}

// Singleton instance
export const PluginRegistry = new PluginRegistryImpl();