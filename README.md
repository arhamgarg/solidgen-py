# SolidWorks MCP (Python)

This project implements an MCP server that provides a powerful tool for generating SolidWorks automation scripts using Python and the `pywin32` library. It leverages a Large Language Model (LLM) to interpret user requests and produce runnable Python code for creating parts and drawings in SolidWorks.

## Features

- **SolidWorks Automation:** Generate Python scripts to automate tasks within SolidWorks.
- **LLM-Powered Code Generation:** Utilizes an LLM to translate natural language requests into `pywin32` code.
- **Easy Integration:** Designed as a FastMCP server, allowing seamless integration with MCP-compatible clients and assistants.
- **Timestamped Saving:** Generated scripts include logic to save SolidWorks parts with unique, timestamped filenames.

## How it Works

The `solidgen` tool exposed by this server takes a user request as input. It then constructs a detailed prompt for an LLM, instructing it to generate a Python script that uses `pywin32` to perform the requested SolidWorks operation. The generated script includes boilerplate for initializing SolidWorks and saving the created part.

## Getting Started

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/arhamgarg/solidgen-py.git
   cd solidgen-py
   ```
2. Install dependencies using `uv`:
   ```bash
   uv sync
   ```

### Running the Server

To run the FastMCP server:

```bash
fastmcp run src/server.py
```

Once running, the server will expose the `solidgen` tool, which can be called by an MCP client.

## Usage (via an MCP Client)

An MCP client can call the `solidgen` tool with a `user_request` string.

Example of how an MCP client might call the tool:

```json
{
  "mcpServers": {
    "solidgen-py": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/solidgen-py/src",
        "run",
        "server.py"
      ]
    }
  }
}
```

The tool will return a Markdown-formatted Python code block containing the generated SolidWorks automation script.
