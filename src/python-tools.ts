/**
 * Python Tools Interface for Raycast Extension
 * Provides TypeScript wrappers for Python developer tools
 */

import { exec } from "child_process";
import { promisify } from "util";
import path from "path";
import fs from "fs";

const execAsync = promisify(exec);

// Get the path to the Python tools directory
// Try multiple possible locations for the Python script
function getPythonToolsPath(): string {
  const possiblePaths = [
    path.join(__dirname, "..", "assets", "devtools.py"),  // Bundled with extension
    path.join(__dirname, "..", "python-tools", "devtools.py"),  // Development
    "***REMOVED***/Documents/raycast/devtoolkit/python-tools/devtools.py"  // Absolute fallback
  ];
  
  for (const scriptPath of possiblePaths) {
    if (fs.existsSync(scriptPath)) {
      return scriptPath;
    }
  }
  
  throw new Error("Python devtools script not found in any expected location");
}

const PYTHON_TOOLS_PATH = getPythonToolsPath();

export interface EpochResult {
  epoch: number;
  utc: {
    readable: string;
    iso: string;
    ddmmyyyy: string;
  };
  local: {
    readable: string;
    iso: string;
    ddmmyyyy: string;
  };
  relative: {
    days: number;
    seconds: number;
    human: string;
  };
}

export interface JWTResult {
  header: any;
  payload: any;
  signature_length: number;
  issued_at_readable?: string;
  expires_at_readable?: string;
  is_expired?: boolean;
  expires_in_seconds?: number;
}

export interface UrlResult {
  input: string;
  output: string;
  operation: "encode" | "decode";
  is_valid_url: boolean;
}

export interface Base64Result {
  input: string;
  output: string;
  operation: "encode" | "decode";
}

export interface HashResult {
  input: string;
  algorithm: string;
  hash: string;
}

export interface JsonResult {
  input: string;
  output?: string;
  operation?: "format" | "minify";
  valid: boolean;
  error?: string;
}

export interface UuidResult {
  version: number;
  count: number;
  uuids: string[];
}

export interface ColorResult {
  input: string;
  hex: string;
  rgb: string;
  hsl: string;
  values: {
    r: number;
    g: number;
    b: number;
    h: number;
    s: number;
    l: number;
  };
}

class PythonToolsError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "PythonToolsError";
  }
}

/**
 * Execute Python tool command
 */
async function executePythonTool(command: string, args: string[] = []): Promise<any> {
  try {
    const fullCommand = `python3 "${PYTHON_TOOLS_PATH}" ${command} ${args.map(arg => `"${arg}"`).join(" ")}`;
    console.log(`Executing: ${fullCommand}`); // Debug log
    
    const { stdout, stderr } = await execAsync(fullCommand);
    
    if (stderr) {
      console.error(`Python tool stderr: ${stderr}`); // Debug log
      throw new PythonToolsError(stderr.trim());
    }
    
    console.log(`Python tool stdout: ${stdout}`); // Debug log
    return JSON.parse(stdout);
  } catch (error) {
    console.error(`Python tool error: ${error}`); // Debug log
    if (error instanceof SyntaxError) {
      throw new PythonToolsError(`Invalid JSON response from Python tool: ${error.message}`);
    }
    throw error;
  }
}

/**
 * Python Tools API
 */
export class PythonTools {
  /**
   * Convert epoch timestamp to readable formats
   */
  static async convertEpoch(timestamp?: string): Promise<EpochResult> {
    const args = timestamp ? [timestamp] : [];
    return executePythonTool("epoch", args);
  }

  /**
   * Decode JWT token
   */
  static async decodeJWT(token: string): Promise<JWTResult> {
    return executePythonTool("jwt", [token]);
  }

  /**
   * URL encode or decode
   */
  static async urlEncode(text: string, decode: boolean = false): Promise<UrlResult> {
    const args = decode ? [text, "--decode"] : [text];
    return executePythonTool("url", args);
  }

  /**
   * Base64 encode or decode
   */
  static async base64Convert(text: string, decode: boolean = false): Promise<Base64Result> {
    const args = decode ? [text, "--decode"] : [text];
    return executePythonTool("base64", args);
  }

  /**
   * Generate hash
   */
  static async generateHash(text: string, algorithm: "md5" | "sha1" | "sha256" | "sha512" = "sha256"): Promise<HashResult> {
    return executePythonTool("hash", [text, "--algorithm", algorithm]);
  }

  /**
   * Format or minify JSON
   */
  static async formatJson(text: string, minify: boolean = false): Promise<JsonResult> {
    const args = minify ? [text, "--minify"] : [text];
    return executePythonTool("json", args);
  }

  /**
   * Generate UUID
   */
  static async generateUuid(version: 1 | 4 = 4, count: number = 1): Promise<UuidResult> {
    return executePythonTool("uuid", ["--version", version.toString(), "--count", count.toString()]);
  }

  /**
   * Convert color formats
   */
  static async convertColor(color: string): Promise<ColorResult> {
    return executePythonTool("color", [color]);
  }
}

/**
 * Utility functions for common operations
 */
export class DevToolsUtils {
  /**
   * Copy text to clipboard and show toast
   */
  static async copyToClipboard(text: string, message?: string): Promise<void> {
    const { Clipboard, showToast, Toast } = await import("@raycast/api");
    await Clipboard.copy(text);
    await showToast({
      style: Toast.Style.Success,
      title: message || "Copied to clipboard",
    });
  }

  /**
   * Show error toast
   */
  static async showError(error: Error): Promise<void> {
    const { showToast, Toast } = await import("@raycast/api");
    await showToast({
      style: Toast.Style.Failure,
      title: "Error",
      message: error.message,
    });
  }

  /**
   * Format timestamp for display
   */
  static formatTimestamp(epochResult: EpochResult): string {
    return `Local: ${epochResult.local.readable}\nUTC: ${epochResult.utc.readable}\nRelative: ${epochResult.relative.human}`;
  }

  /**
   * Format JWT payload for display
   */
  static formatJWTInfo(jwtResult: JWTResult): string {
    const lines = [
      `Algorithm: ${jwtResult.header.alg || "Unknown"}`,
      `Type: ${jwtResult.header.typ || "Unknown"}`,
    ];

    if (jwtResult.payload.sub) lines.push(`Subject: ${jwtResult.payload.sub}`);
    if (jwtResult.payload.iss) lines.push(`Issuer: ${jwtResult.payload.iss}`);
    if (jwtResult.payload.aud) lines.push(`Audience: ${jwtResult.payload.aud}`);
    if (jwtResult.issued_at_readable) lines.push(`Issued: ${jwtResult.issued_at_readable}`);
    if (jwtResult.expires_at_readable) lines.push(`Expires: ${jwtResult.expires_at_readable}`);
    if (jwtResult.is_expired !== undefined) lines.push(`Status: ${jwtResult.is_expired ? "Expired" : "Valid"}`);

    return lines.join("\n");
  }
}

export { PythonToolsError };