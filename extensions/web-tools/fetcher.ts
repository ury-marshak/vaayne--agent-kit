import { mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import {
  DEFAULT_MAX_BYTES,
  DEFAULT_MAX_LINES,
  formatSize,
  type TruncationResult,
  truncateHead,
  withFileMutationQueue,
} from "@mariozechner/pi-coding-agent";
import { JSDOM } from "jsdom";
import TurndownService from "turndown";

export type FetchFormat = "markdown" | "text" | "html" | "json";

export type FetchParams = {
  url: string;
  headers?: Record<string, string>;
};

export type FetchResult = {
  content: string;
  isError: boolean;
  truncation?: TruncationResult;
  fullOutputPath?: string;
};

const DEFAULT_USER_AGENT =
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36";

async function writeFullOutputToTempFile(content: string): Promise<string> {
  const tempDir = await mkdtemp(join(tmpdir(), "pi-web-fetch-"));
  const tempFile = join(tempDir, "output.txt");

  await withFileMutationQueue(tempFile, async () => {
    await writeFile(tempFile, content, "utf8");
  });

  return tempFile;
}

async function createSuccessResult(content: string): Promise<FetchResult> {
  const truncation = truncateHead(content, {
    maxLines: DEFAULT_MAX_LINES,
    maxBytes: DEFAULT_MAX_BYTES,
  });

  if (!truncation.truncated) {
    return {
      content: truncation.content,
      isError: false,
    };
  }

  const fullOutputPath = await writeFullOutputToTempFile(content);
  const omittedLines = truncation.totalLines - truncation.outputLines;
  const omittedBytes = truncation.totalBytes - truncation.outputBytes;

  let resultText = truncation.content;
  resultText += `\n\n[Output truncated: showing ${truncation.outputLines} of ${truncation.totalLines} lines`;
  resultText += ` (${formatSize(truncation.outputBytes)} of ${formatSize(truncation.totalBytes)}).`;
  resultText += ` ${omittedLines} lines (${formatSize(omittedBytes)}) omitted.`;
  resultText += ` Full output saved to: ${fullOutputPath}]`;

  return {
    content: resultText,
    isError: false,
    truncation,
    fullOutputPath,
  };
}

async function fetchUrl(params: FetchParams): Promise<Response> {
  const { url, headers } = params;

  const response = await fetch(url, {
    headers: {
      "User-Agent": DEFAULT_USER_AGENT,
      ...headers,
    },
  });

  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status} ${response.statusText}`);
  }

  return response;
}

export async function fetchHtml(params: FetchParams): Promise<FetchResult> {
  try {
    const response = await fetchUrl(params);
    const html = await response.text();
    return await createSuccessResult(html);
  } catch (error) {
    return {
      content: error instanceof Error ? error.message : String(error),
      isError: true,
    };
  }
}

export async function fetchJson(params: FetchParams): Promise<FetchResult> {
  try {
    const response = await fetchUrl(params);
    const json = await response.json();
    return await createSuccessResult(JSON.stringify(json, null, 2));
  } catch (error) {
    return {
      content: error instanceof Error ? error.message : String(error),
      isError: true,
    };
  }
}

export async function fetchText(params: FetchParams): Promise<FetchResult> {
  try {
    const response = await fetchUrl(params);
    const html = await response.text();

    const dom = new JSDOM(html);
    const document = dom.window.document;

    // Remove script and style elements
    for (const el of document.querySelectorAll("script")) {
      el.remove();
    }
    for (const el of document.querySelectorAll("style")) {
      el.remove();
    }

    // Extract and normalize text
    const text = document.body?.textContent || "";
    const normalizedText = text.replace(/\s+/g, " ").trim();

    return await createSuccessResult(normalizedText);
  } catch (error) {
    return {
      content: error instanceof Error ? error.message : String(error),
      isError: true,
    };
  }
}

export async function fetchMarkdown(params: FetchParams): Promise<FetchResult> {
  try {
    const response = await fetchUrl(params);
    const html = await response.text();

    const dom = new JSDOM(html);
    const document = dom.window.document;

    // Remove script, style, nav, footer elements for cleaner output
    const removeSelectors = [
      "script",
      "style",
      "nav",
      "footer",
      "header",
      "aside",
    ];
    for (const selector of removeSelectors) {
      for (const el of document.querySelectorAll(selector)) {
        el.remove();
      }
    }

    const turndownService = new TurndownService({
      headingStyle: "atx",
      codeBlockStyle: "fenced",
    });

    // Get main content or body
    const main = document.querySelector("main, article, .content, #content");
    const contentElement = main || document.body;

    const markdown = turndownService.turndown(contentElement?.innerHTML || "");

    return await createSuccessResult(markdown);
  } catch (error) {
    return {
      content: error instanceof Error ? error.message : String(error),
      isError: true,
    };
  }
}
