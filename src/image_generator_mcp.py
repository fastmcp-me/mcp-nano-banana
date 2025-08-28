import asyncio
import logging
import os
import base64
import uuid
import json
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- MCP Server Setup ---
# Create a FastMCP server instance
mcp = FastMCP(
    name="image_generator_mcp_server",
)
logger.info(f"MCP server '{mcp.name}' created.")


# --- Tool Definition ---
@mcp.tool(
    name="generate_image",
    description="Generates an image based on a text prompt using the Gemini API and returns the image as a base64 encoded string.",
)
async def generate_image(prompt: str) -> str:
    """
    Generates an image from a text prompt and returns the base64 encoded PNG data.
    """
    try:
        logger.info(f"Tool 'generate_image' called with prompt: '{prompt}'")

        model = genai.GenerativeModel('gemini-2.5-flash-image-preview')

        response = await model.generate_content_async([f"Generate a high-quality, detailed image of: {prompt}"])

        if not response.parts:
            logger.error("API response did not contain any parts.")
            raise Exception("Failed to generate image: API response was empty.")

        image_data_base64 = response.parts[0].inline_data.data

        # Save the image locally for auditing/debugging
        filename = f"{uuid.uuid4()}.png"
        filepath = os.path.join("public", filename)
        with open(filepath, "wb") as f:
            f.write(base64.b64decode(image_data_base64))
        logger.info(f"Image saved locally to {filepath}")

        # Return the base64 encoded image data as a string
        return image_data_base64

    except Exception as e:
        logger.error(f"An error occurred during image generation: {e}")
        return json.dumps({"error": f"An error occurred: {str(e)}"})
    

def main():
    # Get the API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set or .env file is missing.")
    # Configure the Gemini API client
    genai.configure(api_key=api_key)
    logger.info("Gemini API configured successfully.")

    logger.info("Starting MCP server via mcp.run()...")
    asyncio.run(mcp.run())

if __name__ == "__main__":
    main()