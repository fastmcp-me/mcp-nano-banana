# MCP Image Generator

This project is an MCP (Model Context Protocol) server that generates images using the Google Gemini API.

## Description

This server implements the Model Context Protocol to expose a single tool, `generate_image`, to a compatible AI model. The tool accepts a text prompt, uses the Google Gemini API to generate an image, saves the image to the `public/` directory for auditing, and returns the raw image data as a base64-encoded string.

## Setup

### 1. Dependencies

This project uses Python and its dependencies are defined in `pyproject.toml`. You can install them using `pip`:

```bash
pip install .
```

This will install `mcp`, `google-generativeai`, and other required packages.

### 2. API Key

You need a Google Gemini API key to use this server.

1.  Create a file named `.env` in the root of the project.
2.  Add your API key to the `.env` file in the following format:

    ```
    GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

## Running the Server

This server is designed to be run as a subprocess by an MCP client or using the `mcp` command-line tool. The server listens for requests on `stdio`.

To run the server manually for testing or integration, use the following command:

```bash
mcp run --transport stdio src/image_generator_mcp.py:mcp
```

The server will start and wait for a JSON-RPC request on its standard input.

## How It Works

The server defines a `FastMCP` instance named `mcp`. It exposes one tool:

-   `generate_image(prompt: str) -> str`: Takes a string `prompt` and returns a base64-encoded PNG image as a string.
