# MCP Extension

A Pi extension that connects to MCP (Model Context Protocol) servers and provides tools to interact with them.

## Tools

### `mcp_list`

List all available MCP tools with names and descriptions.

### `mcp_inspect`

Show full tool signature as a JSDoc function stub.

**Parameters:**

| Name   | Type   | Required | Description                     |
| ------ | ------ | -------- | ------------------------------- |
| `tool` | string | Yes      | Name of the MCP tool to inspect |

### `mcp_invoke`

Call a single MCP tool with JSON parameters.

**Parameters:**

| Name     | Type   | Required | Description                    |
| -------- | ------ | -------- | ------------------------------ |
| `tool`   | string | Yes      | Name of the MCP tool to invoke |
| `params` | object | No       | Parameters to pass to the tool |

### `mcp_exec`

Execute JavaScript code to orchestrate multiple MCP tool calls with logic.

**Parameters:**

| Name   | Type   | Required | Description                                        |
| ------ | ------ | -------- | -------------------------------------------------- |
| `code` | string | Yes      | JavaScript code using `mcp.callTool(name, params)` |

## Configuration

Create `~/.pi/agent/mcp.json` to configure MCP servers.

## Requirements

- `mh` CLI must be installed and available in PATH
