#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "click",
#     "rich",
#     "google-genai",
#     "Pillow",
# ]
# ///

"""CLI for image generation and understanding using Google Vertex AI Gemini models."""

import logging
import mimetypes
import os
from io import BytesIO
from pathlib import Path

import click
from google import genai
from google.genai import types
from PIL import Image
from rich.console import Console
from rich.logging import RichHandler

LOG_DIR = Path(".agents/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(console=Console(stderr=True)),
        logging.FileHandler(LOG_DIR / "vertex_ai_image.log"),
    ],
)
logger = logging.getLogger(__name__)

DEFAULT_GENERATE_MODEL = "gemini-3.1-flash-image-preview"
DEFAULT_READ_MODEL = "gemini-2.5-flash"

SAFETY_OFF = [
    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
]


def _make_client() -> genai.Client:
    api_key = os.environ.get("GOOGLE_CLOUD_API_KEY")
    if not api_key:
        raise click.ClickException(
            "GOOGLE_CLOUD_API_KEY not set. Export it first:\n"
            "  export GOOGLE_CLOUD_API_KEY=your-key-here"
        )
    return genai.Client(
        vertexai=True,
        api_key=api_key,
    )


@click.group()
def cli() -> None:
    """Generate or read images with Vertex AI Gemini models."""


@cli.command()
@click.option("--prompt", "-p", required=True, help="Text prompt describing the image to generate.")
@click.option("--output", "-o", default="output/generated.png", help="Output file path (png/jpg).")
@click.option("--model", "-m", default=DEFAULT_GENERATE_MODEL, help=f"Model ID. Default: {DEFAULT_GENERATE_MODEL}")
@click.option("--dry-run", is_flag=True, help="Preview the request without calling the API.")
def generate(prompt: str, output: str, model: str, dry_run: bool) -> None:
    """Generate an image from a text prompt."""
    logger.info("Generate image — model=%s", model)
    logger.info("Prompt: %s", prompt)
    logger.info("Output: %s", output)

    if dry_run:
        logger.info("[DRY RUN] Would call %s with the above prompt.", model)
        return

    client = _make_client()

    config = types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        safety_settings=SAFETY_OFF,
    )

    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    saved = False
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=prompt,
        config=config,
    ):
        if chunk.candidates:
            for part in chunk.candidates[0].content.parts:
                if part.text:
                    click.echo(part.text, nl=False)
                elif part.inline_data:
                    image = Image.open(BytesIO(part.inline_data.data))
                    image.save(str(out_path))
                    logger.info("Image saved to %s", out_path)
                    saved = True

    click.echo()  # final newline after streaming text

    if not saved:
        logger.warning("No image data returned by the model.")


@cli.command()
@click.option("--image", "-i", required=True, help="Local file path or gs:// URI of the image.")
@click.option("--prompt", "-p", default="Describe this image in detail.", help="Question or instruction about the image.")
@click.option("--model", "-m", default=DEFAULT_READ_MODEL, help=f"Model ID. Default: {DEFAULT_READ_MODEL}")
@click.option("--dry-run", is_flag=True, help="Preview the request without calling the API.")
def read(image: str, prompt: str, model: str, dry_run: bool) -> None:
    """Read and describe an image (local file or GCS URI)."""
    logger.info("Read image — model=%s", model)
    logger.info("Image: %s", image)
    logger.info("Prompt: %s", prompt)

    if dry_run:
        logger.info("[DRY RUN] Would call %s with the above inputs.", model)
        return

    client = _make_client()

    if image.startswith("gs://"):
        mime = mimetypes.guess_type(image)[0] or "image/jpeg"
        image_part = types.Part.from_uri(file_uri=image, mime_type=mime)
    else:
        img_path = Path(image)
        if not img_path.exists():
            raise click.ClickException(f"File not found: {image}")
        mime = mimetypes.guess_type(str(img_path))[0] or "image/jpeg"
        data = img_path.read_bytes()
        image_part = types.Part.from_bytes(data=data, mime_type=mime)

    response = client.models.generate_content(
        model=model,
        contents=[prompt, image_part],
    )

    click.echo(response.text)


if __name__ == "__main__":
    cli()
