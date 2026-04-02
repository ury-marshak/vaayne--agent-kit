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

"""CLI for image generation, editing, and understanding using Google Gemini models."""

import logging
import mimetypes
import os
import re
from datetime import datetime
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

DEFAULT_OUTPUT_DIR = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "vertex-ai-images"


def _default_output(prefix: str, prompt: str) -> str:
    """Build a default output path like generate-20260402-134500-cat-astronaut.png."""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    slug = re.sub(r"[^a-z0-9]+", "-", prompt.lower()).strip("-")[:48].rstrip("-")
    return str(DEFAULT_OUTPUT_DIR / f"{prefix}-{ts}-{slug}.png")

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

MODEL_GENERATE = "gemini-3.1-flash-image-preview"
MODEL_PRO = "gemini-3-pro-image-preview"
MODEL_FAST = "gemini-2.5-flash-image"
MODEL_READ = "gemini-2.5-flash"

ASPECT_RATIOS = [
    "1:1", "1:4", "1:8", "2:3", "3:2", "3:4",
    "4:1", "4:3", "4:5", "5:4", "8:1",
    "9:16", "16:9", "21:9",
]

IMAGE_SIZES = ["512", "1K", "2K", "4K"]

THINKING_LEVELS = ["minimal", "high"]


def _make_client() -> genai.Client:
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_CLOUD_API_KEY")
    if not api_key:
        raise click.ClickException(
            "API key not set. Export one of:\n"
            "  export GEMINI_API_KEY=your-key-here\n"
            "  export GOOGLE_CLOUD_API_KEY=your-key-here"
        )
    return genai.Client(api_key=api_key)


def _load_image_part(image_path: str) -> types.Part | Image.Image:
    """Load an image from a local path or GCS URI."""
    if image_path.startswith("gs://"):
        mime = mimetypes.guess_type(image_path)[0] or "image/jpeg"
        return types.Part.from_uri(file_uri=image_path, mime_type=mime)
    img_path = Path(image_path)
    if not img_path.exists():
        raise click.ClickException(f"File not found: {image_path}")
    return Image.open(img_path)


def _build_image_config(
    aspect_ratio: str | None,
    size: str | None,
) -> types.ImageConfig | None:
    if not aspect_ratio and not size:
        return None
    kwargs: dict = {}
    if aspect_ratio:
        kwargs["aspect_ratio"] = aspect_ratio
    if size:
        kwargs["image_size"] = size
    return types.ImageConfig(**kwargs)


def _build_config(
    *,
    image_only: bool = False,
    aspect_ratio: str | None = None,
    size: str | None = None,
    thinking_level: str | None = None,
) -> types.GenerateContentConfig:
    modalities = ["IMAGE"] if image_only else ["TEXT", "IMAGE"]
    image_config = _build_image_config(aspect_ratio, size)

    kwargs: dict = {"response_modalities": modalities}
    if image_config:
        kwargs["image_config"] = image_config
    if thinking_level:
        kwargs["thinking_config"] = types.ThinkingConfig(
            thinking_level=thinking_level.capitalize(),
        )
    return types.GenerateContentConfig(**kwargs)


def _save_response(response, output: str) -> None:
    """Extract text and images from a generate_content response."""
    out_path = Path(output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    saved = False
    img_index = 0

    for part in response.parts:
        if getattr(part, "thought", False):
            continue
        if part.text is not None:
            click.echo(part.text)
        elif part.inline_data is not None:
            if img_index == 0:
                save_path = out_path
            else:
                save_path = out_path.with_stem(f"{out_path.stem}_{img_index}")
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(str(save_path))
            logger.info("Image saved to %s (%dx%d)", save_path, image.width, image.height)
            saved = True
            img_index += 1

    if not saved:
        logger.warning("No image data returned by the model.")


@click.group()
def cli() -> None:
    """Generate, edit, or read images with Google Gemini models."""


@cli.command()
@click.option("--prompt", "-p", required=True, help="Text prompt describing the image to generate.")
@click.option("--output", "-o", default=None, help="Output file path (default: $XDG_CACHE_HOME/vertex-ai-images/generated.png).")
@click.option("--model", "-m", default=MODEL_GENERATE, help=f"Model ID (default: {MODEL_GENERATE}).")
@click.option("--aspect-ratio", "-a", type=click.Choice(ASPECT_RATIOS), default=None, help="Output aspect ratio.")
@click.option("--size", "-s", type=click.Choice(IMAGE_SIZES), default=None, help="Output resolution (512, 1K, 2K, 4K).")
@click.option("--image-only", is_flag=True, help="Return only image, no text.")
@click.option("--thinking-level", "-t", type=click.Choice(THINKING_LEVELS), default=None, help="Thinking level (minimal or high).")
@click.option("--dry-run", is_flag=True, help="Preview the request without calling the API.")
def generate(
    prompt: str,
    output: str,
    model: str,
    aspect_ratio: str | None,
    size: str | None,
    image_only: bool,
    thinking_level: str | None,
    dry_run: bool,
) -> None:
    """Generate an image from a text prompt."""
    if output is None:
        output = _default_output("generate", prompt)
    logger.info("Generate — model=%s", model)
    logger.info("Prompt: %s", prompt)
    if aspect_ratio:
        logger.info("Aspect ratio: %s", aspect_ratio)
    if size:
        logger.info("Size: %s", size)

    if dry_run:
        logger.info("[DRY RUN] Would call %s with the above settings.", model)
        return

    client = _make_client()
    config = _build_config(
        image_only=image_only,
        aspect_ratio=aspect_ratio,
        size=size,
        thinking_level=thinking_level,
    )

    response = client.models.generate_content(
        model=model,
        contents=[prompt],
        config=config,
    )

    _save_response(response, output)


@cli.command()
@click.option("--prompt", "-p", required=True, help="Edit instruction for the image(s).")
@click.option("--image", "-i", "images", required=True, multiple=True, help="Input image path(s) or gs:// URI(s). Repeat for multiple images (up to 14).")
@click.option("--output", "-o", default=None, help="Output file path (default: $XDG_CACHE_HOME/vertex-ai-images/edited.png).")
@click.option("--model", "-m", default=MODEL_GENERATE, help=f"Model ID (default: {MODEL_GENERATE}).")
@click.option("--aspect-ratio", "-a", type=click.Choice(ASPECT_RATIOS), default=None, help="Output aspect ratio.")
@click.option("--size", "-s", type=click.Choice(IMAGE_SIZES), default=None, help="Output resolution (512, 1K, 2K, 4K).")
@click.option("--image-only", is_flag=True, help="Return only image, no text.")
@click.option("--thinking-level", "-t", type=click.Choice(THINKING_LEVELS), default=None, help="Thinking level (minimal or high).")
@click.option("--dry-run", is_flag=True, help="Preview the request without calling the API.")
def edit(
    prompt: str,
    images: tuple[str, ...],
    output: str,
    model: str,
    aspect_ratio: str | None,
    size: str | None,
    image_only: bool,
    thinking_level: str | None,
    dry_run: bool,
) -> None:
    """Edit image(s) using a text prompt. Supports up to 14 reference images."""
    if output is None:
        output = _default_output("edit", prompt)
    logger.info("Edit — model=%s", model)
    logger.info("Prompt: %s", prompt)
    logger.info("Input images: %s", ", ".join(images))

    if len(images) > 14:
        raise click.ClickException("Maximum 14 reference images allowed.")

    if dry_run:
        logger.info("[DRY RUN] Would call %s with the above settings.", model)
        return

    client = _make_client()
    config = _build_config(
        image_only=image_only,
        aspect_ratio=aspect_ratio,
        size=size,
        thinking_level=thinking_level,
    )

    contents: list = [prompt]
    for img_path in images:
        contents.append(_load_image_part(img_path))

    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=config,
    )

    _save_response(response, output)


@cli.command()
@click.option("--image", "-i", required=True, help="Local file path or gs:// URI of the image.")
@click.option("--prompt", "-p", default="Describe this image in detail.", help="Question or instruction about the image.")
@click.option("--model", "-m", default=MODEL_READ, help=f"Model ID (default: {MODEL_READ}).")
@click.option("--dry-run", is_flag=True, help="Preview the request without calling the API.")
def read(image: str, prompt: str, model: str, dry_run: bool) -> None:
    """Read and describe an image (local file or GCS URI)."""
    logger.info("Read — model=%s", model)
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
