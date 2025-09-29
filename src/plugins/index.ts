/**
 * Plugin Index
 * Registers all available plugins with the registry
 */

import { PluginRegistry } from "./registry";

// Import all plugins
import { Base64Plugin } from "./encoding/base64";
import { UrlPlugin } from "./encoding/url";
import { JWTPlugin } from "./security/jwt";
import { HashPlugin } from "./security/hash";
import { UuidPlugin } from "./text/uuid";
import { JsonPlugin } from "./text/json";
import { TimestampPlugin } from "./time/timestamp";

// Plugin registration function
export function registerAllPlugins() {
  console.log("Registering all plugins...");
  
  try {
    // Register encoding plugins
    PluginRegistry.registerPlugin(Base64Plugin);
    PluginRegistry.registerPlugin(UrlPlugin);
    
    // Register security plugins
    PluginRegistry.registerPlugin(JWTPlugin);
    PluginRegistry.registerPlugin(HashPlugin);
    
    // Register text/data plugins
    PluginRegistry.registerPlugin(UuidPlugin);
    PluginRegistry.registerPlugin(JsonPlugin);
    
    // Register time plugins
    PluginRegistry.registerPlugin(TimestampPlugin);
    
    console.log(`Successfully registered ${PluginRegistry.listPlugins().length} plugins`);
  } catch (error) {
    console.error("Failed to register plugins:", error);
    throw error;
  }
}

// Export registry for use in components
export { PluginRegistry };
export * from "./types";
export * from "./base";