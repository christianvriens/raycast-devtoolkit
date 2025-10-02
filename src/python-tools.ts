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
    "/Users/shm/Documents/raycast/devtoolkit/python-tools/devtools.py"  // Absolute fallback
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
  // Prefer a project-local virtualenv if present (created by python-tools/run.sh)
  const venvPython = path.join(path.dirname(PYTHON_TOOLS_PATH), ".venv", "bin", "python");
  const pythonCandidates = [venvPython, "python3", "python", "/usr/bin/python3"];
  const attempts: Array<{bin: string; error?: any; stdout?: string; stderr?: string}> = [];

  for (const bin of pythonCandidates) {
    const fullCommand = `${bin} "${PYTHON_TOOLS_PATH}" ${command} ${args.map(arg => `"${arg}"`).join(" ")}`;
    console.log(`Attempting to execute: ${fullCommand}`);

    try {
      const { stdout, stderr } = await execAsync(fullCommand);

      // If Python wrote to stderr, capture it and treat as an error (it may contain a traceback)
      if (stderr && stderr.trim().length > 0) {
        const msg = `Python tool wrote to stderr using ${bin}: ${stderr.trim()}`;
        // write a log and throw
        const logsDir = path.join(path.dirname(PYTHON_TOOLS_PATH), "logs");
        try { fs.mkdirSync(logsDir, { recursive: true }); } catch (e) { /* best-effort */ }
        const logFile = path.join(logsDir, `python-tool-${Date.now()}.log`);
        const content = [
          `COMMAND: ${fullCommand}`,
          `STDOUT:\n${stdout || ""}`,
          `STDERR:\n${stderr}`,
        ].join("\n\n");
        try { fs.writeFileSync(logFile, content, { encoding: "utf8" }); } catch (e) { console.error("Failed to write python tool log:", e); }

        throw new PythonToolsError(`${msg}. See log: ${logFile}`);
      }

      // Success path: parse stdout
      console.log(`Python tool stdout (from ${bin}): ${stdout}`);
      return JSON.parse(stdout);
    } catch (err: any) {
      // Record attempt details for later reporting
      attempts.push({ bin, error: err, stdout: err && err.stdout, stderr: err && err.stderr });
      console.error(`Execution with ${bin} failed:`, err && (err.message || err));
      // Try next candidate
    }
  }

  // If we reach here, all attempts failed. Write a consolidated log with details to help debugging.
  const logsDir = path.join(path.dirname(PYTHON_TOOLS_PATH), "logs");
  try { fs.mkdirSync(logsDir, { recursive: true }); } catch (e) { /* best-effort */ }
  const logFile = path.join(logsDir, `python-tool-failed-${Date.now()}.log`);
  const parts: string[] = [];
  parts.push(`All python execution attempts failed when running: ${command} ${args.join(" ")}`);
  parts.push(`Tried candidates: ${pythonCandidates.join(", ")}`);
  for (const a of attempts) {
    parts.push(`--- ATTEMPT: ${a.bin} ---`);
    parts.push(`ERROR: ${a.error && (a.error.message || String(a.error))}`);
    parts.push(`STDOUT:\n${a.stdout || ""}`);
    parts.push(`STDERR:\n${a.stderr || ""}`);
  }
  const logContent = parts.join("\n\n");
  try { fs.writeFileSync(logFile, logContent, { encoding: "utf8" }); } catch (e) { console.error("Failed to write consolidated python tool log:", e); }

  // Throw a helpful error that Raycast will show; include path to the log for full traceback
  throw new PythonToolsError(`Failed to execute Python tool (tried python3/python). See detailed log: ${logFile}`);
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