---
name: vertex-ai-image
description: >
  Generate or understand images using Google Vertex AI Gemini models.
  Use when asked to "generate an image", "create a picture", "describe an image",
  "what's in this image", "analyze this photo", "image to text", "text to image",
  "explain this screenshot", "visual question answering", or any task involving
  image generation, image description, or visual understanding.
---

# Vertex AI Image CLI

A Python CLI for image generation and understanding via Google Vertex AI Gemini.

## Prerequisites

Set `GOOGLE_CLOUD_API_KEY`:

```bash
export GOOGLE_CLOUD_API_KEY=your-key-here
```

## Commands

### Generate an image from text

```bash
uv run --script scripts/vertex_ai_image.py generate \
  --prompt "A cat astronaut floating in space" \
  --output output/cat-astronaut.png
```

Options:
- `--prompt, -p` — Text prompt (required)
- `--output, -o` — Output file path (default: `output/generated.png`)
- `--model, -m` — Model override (default: `gemini-3.1-flash-image-preview`)
- `--dry-run` — Preview without API call

### Read/describe an image

```bash
# Local file
uv run --script scripts/vertex_ai_image.py read \
  --image photo.jpg \
  --prompt "What objects are in this image?"

# GCS URI
uv run --script scripts/vertex_ai_image.py read \
  --image gs://bucket/image.jpg
```

Options:
- `--image, -i` — Local path or `gs://` URI (required)
- `--prompt, -p` — Question about the image (default: "Describe this image in detail.")
- `--model, -m` — Model override (default: `gemini-2.5-flash`)
- `--dry-run` — Preview without API call

## Models

| Task | Default Model |
|---|---|
| Image generation | `gemini-3.1-flash-image-preview` |
| Image reading | `gemini-2.5-flash` |
