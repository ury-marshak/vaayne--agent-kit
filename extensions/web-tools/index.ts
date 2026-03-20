/**
 * Web Tools Extension for Pi
 *
 * Provides web-fetch and web-search tools.
 *
 * Environment variables:
 * - EXA_API_KEY: Optional, for authenticated Exa API access
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Text } from "@mariozechner/pi-tui";
import { Type } from "@sinclair/typebox";
import {
  type FetchFormat,
  fetchHtml,
  fetchJson,
  fetchMarkdown,
  type FetchResult,
  fetchText,
} from "./fetcher.js";
import { search } from "./searcher.js";

const FETCH_PREVIEW_MAX_LINES = 10;
const FETCH_PREVIEW_MAX_BYTES = 1024;
const FETCH_EXPANDED_PREVIEW_MAX_LINES = 50;
const FETCH_EXPANDED_PREVIEW_MAX_BYTES = 5 * 1024;

function getTextContent(result: { content: Array<{ type: string; text?: string }> }): string {
  return result.content
    .filter((item) => item.type === "text")
    .map((item) => item.text ?? "")
    .join("\n");
}

function getCompactPreview(
  text: string,
  maxLines: number,
  maxBytes: number,
): { preview: string; totalLines: number; previewLines: number; truncated: boolean } {
  const normalized = text.trim();
  if (!normalized) {
    return {
      preview: "",
      totalLines: 0,
      previewLines: 0,
      truncated: false,
    };
  }

  const lines = normalized.split("\n");
  const previewLines: string[] = [];
  let usedBytes = 0;
  let truncated = false;

  for (const line of lines) {
    if (previewLines.length >= maxLines) {
      truncated = true;
      break;
    }

    const prefix = previewLines.length > 0 ? "\n" : "";
    const lineWithPrefix = `${prefix}${line}`;
    const lineBytes = Buffer.byteLength(lineWithPrefix, "utf8");

    if (usedBytes + lineBytes <= maxBytes) {
      previewLines.push(line);
      usedBytes += lineBytes;
      continue;
    }

    const remainingBytes = maxBytes - usedBytes - Buffer.byteLength(prefix, "utf8");
    if (remainingBytes > 0) {
      let clippedLine = "";
      for (const char of line) {
        const next = clippedLine + char;
        if (Buffer.byteLength(next, "utf8") > remainingBytes) {
          break;
        }
        clippedLine = next;
      }
      previewLines.push(clippedLine);
    }

    truncated = true;
    break;
  }

  return {
    preview: previewLines.join("\n"),
    totalLines: lines.length,
    previewLines: previewLines.length,
    truncated: truncated || previewLines.length < lines.length,
  };
}

export default function webToolsExtension(pi: ExtensionAPI) {
  // Register web-fetch tool
  pi.registerTool({
    name: "web-fetch",
    label: "Web Fetch",
    description:
      "Fetch and extract content from a URL. Returns content in the specified format (markdown by default). Output is truncated when too large; when truncated, the full content is saved to a temp file. Useful for reading web pages, articles, documentation, etc.",
    parameters: Type.Object({
      url: Type.String({ description: "URL to fetch" }),
      format: Type.Optional(
        Type.Union(
          [
            Type.Literal("markdown"),
            Type.Literal("text"),
            Type.Literal("html"),
            Type.Literal("json"),
          ],
          {
            description: "Output format: markdown (default), text, html, or json",
            default: "markdown",
          },
        ),
      ),
      headers: Type.Optional(
        Type.Record(Type.String(), Type.String(), {
          description: "Optional custom headers for the request",
        }),
      ),
    }),

    async execute(_toolCallId, params, _onUpdate, _ctx, _signal) {
      const {
        url,
        format = "markdown",
        headers,
      } = params as {
        url: string;
        format?: FetchFormat;
        headers?: Record<string, string>;
      };

      // Validate URL
      try {
        new URL(url);
      } catch {
        return {
          content: [{ type: "text", text: `Invalid URL: ${url}` }],
          details: {},
          isError: true,
        };
      }

      const fetchParams = { url, headers };

      let result: FetchResult;
      switch (format) {
        case "html":
          result = await fetchHtml(fetchParams);
          break;
        case "json":
          result = await fetchJson(fetchParams);
          break;
        case "text":
          result = await fetchText(fetchParams);
          break;
        default:
          result = await fetchMarkdown(fetchParams);
          break;
      }

      return {
        content: [{ type: "text", text: result.content }],
        details: {
          url,
          format,
          truncation: result.truncation,
          fullOutputPath: result.fullOutputPath,
        },
        isError: result.isError,
      };
    },

    renderCall(args, theme) {
      let text = theme.fg("toolTitle", theme.bold("web-fetch "));
      text += theme.fg("accent", args.url || "...");
      text += theme.fg("muted", ` [${args.format || "markdown"}]`);
      return new Text(text, 0, 0);
    },

    renderResult(result, { expanded, isPartial }, theme) {
      if (isPartial) {
        return new Text(theme.fg("warning", "Fetching..."), 0, 0);
      }

      const details = (result.details ?? {}) as {
        url?: string;
        format?: string;
        truncation?: { truncated?: boolean; totalLines?: number; outputLines?: number };
        fullOutputPath?: string;
      };

      const text = getTextContent(result as { content: Array<{ type: string; text?: string }> });

      if (!text.trim()) {
        return new Text(theme.fg("muted", "No content returned"), 0, 0);
      }

      if (details.fullOutputPath && !expanded) {
        let summary = theme.fg("success", `Fetched ${details.format || "content"}`);
        summary += theme.fg("warning", " (truncated)");
        summary += `\n${theme.fg("muted", `Full output: ${details.fullOutputPath}`)}`;
        summary += `\n${theme.fg("muted", "Expand to preview content")}`;
        return new Text(summary, 0, 0);
      }

      const previewMaxLines = expanded
        ? FETCH_EXPANDED_PREVIEW_MAX_LINES
        : FETCH_PREVIEW_MAX_LINES;
      const previewMaxBytes = expanded
        ? FETCH_EXPANDED_PREVIEW_MAX_BYTES
        : FETCH_PREVIEW_MAX_BYTES;
      const { preview, totalLines, previewLines, truncated } = getCompactPreview(
        text,
        previewMaxLines,
        previewMaxBytes,
      );
      const previewBytes = Buffer.byteLength(preview, "utf8");
      const remainingLines = Math.max(0, totalLines - previewLines);

      let output = "";
      if (details.fullOutputPath) {
        output += theme.fg("warning", "Truncated output") + "\n";
        output += theme.fg("muted", `Full output: ${details.fullOutputPath}`) + "\n\n";
      }

      output += theme.fg("toolOutput", preview);

      if (truncated) {
        output += "\n";
        output += theme.fg(
          "muted",
          `... (preview limited to ${previewMaxLines} lines / ${previewMaxBytes} bytes`,
        );
        if (remainingLines > 0) {
          output += theme.fg("muted", `, ${remainingLines} more lines`);
        }
        output += theme.fg("muted", `, showing ${previewBytes} bytes)`);
      }

      return new Text(output, 0, 0);
    },
  });

  // Register web-search tool
  pi.registerTool({
    name: "web-search",
    label: "Web Search",
    description:
      "Search the web using Exa AI. Returns relevant search results with titles, URLs, and content snippets.",
    parameters: Type.Object({
      query: Type.String({ description: "Search query" }),
      numResults: Type.Optional(
        Type.Number({
          description: "Number of results to return (default: 8)",
          default: 8,
          minimum: 1,
          maximum: 20,
        }),
      ),
    }),

    async execute(_toolCallId, params, _onUpdate, _ctx, _signal) {
      const { query, numResults = 8 } = params as {
        query: string;
        numResults?: number;
      };

      const apiKey = process.env.EXA_API_KEY;
      const response = await search(query, numResults, apiKey);

      if (response.isError) {
        return {
          content: [{ type: "text", text: response.error || "Search failed" }],
          details: {},
          isError: true,
        };
      }

      // Format results as readable text
      const formattedResults = response.results
        .map((r, i) => {
          let entry = `## ${i + 1}. ${r.title}\n`;
          entry += `**URL:** ${r.url}\n`;
          if (r.publishedDate) {
            entry += `**Published:** ${r.publishedDate}\n`;
          }
          if (r.text) {
            entry += `\n${r.text}\n`;
          }
          return entry;
        })
        .join("\n---\n\n");

      const output =
        `# Search Results for: "${query}"\n\nFound ${response.results.length} results.\n\n${formattedResults}`;

      return {
        content: [{ type: "text", text: output }],
        details: { query, resultCount: response.results.length },
        isError: false,
      };
    },
  });
}
