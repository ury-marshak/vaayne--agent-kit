---
name: vertex-ai-image
description: >
  Generate, edit, or understand images using Google Gemini models.
  Use when asked to "generate an image", "create a picture", "edit an image",
  "modify this photo", "describe an image", "what's in this image",
  "analyze this photo", "image to text", "text to image",
  "explain this screenshot", "visual question answering", or any task involving
  image generation, image editing, or visual understanding.
---

# Vertex AI Image CLI

A Python CLI for image generation, editing, and understanding via Google Gemini.

## Prerequisites

Set one of these API keys:

```bash
export GEMINI_API_KEY=your-key-here        # Recommended (Gemini API)
export GOOGLE_CLOUD_API_KEY=your-key-here  # Also supported
```

## Models

| Task                 | Model ID                         | Description                                                 |
| -------------------- | -------------------------------- | ----------------------------------------------------------- |
| Generation (default) | `gemini-3.1-flash-image-preview` | Nano Banana 2 — fast, balanced cost/quality                 |
| Generation (pro)     | `gemini-3-pro-image-preview`     | Nano Banana Pro — professional assets, complex instructions |
| Generation (fast)    | `gemini-2.5-flash-image`         | Nano Banana — high-volume, low-latency                      |
| Image reading        | `gemini-2.5-flash`               | Text understanding model                                    |

## Commands

### Generate an image from text

```bash
# Output defaults to $XDG_CACHE_HOME/vertex-ai-images/generate-{ts}-a-cat-astronaut-floating-in-space.png
uv run --script scripts/vertex_ai_image.py generate \
  --prompt "A cat astronaut floating in space"

# Or specify a custom output path
uv run --script scripts/vertex_ai_image.py generate \
  --prompt "A cat astronaut floating in space" \
  --output output/cat-astronaut.png
```

With aspect ratio and resolution:

```bash
uv run --script scripts/vertex_ai_image.py generate \
  --prompt "A panoramic mountain landscape at sunset" \
  --output output/landscape.png \
  --aspect-ratio 16:9 \
  --size 2K
```

Image-only output (no accompanying text):

```bash
uv run --script scripts/vertex_ai_image.py generate \
  --prompt "A minimalist logo for a coffee shop" \
  --output output/logo.png \
  --image-only
```

With high thinking level for complex prompts:

```bash
uv run --script scripts/vertex_ai_image.py generate \
  --prompt "An infographic explaining photosynthesis as a recipe" \
  --output output/infographic.png \
  --thinking-level high \
  --size 4K
```

Using a different model:

```bash
uv run --script scripts/vertex_ai_image.py generate \
  --prompt "A product photo of a perfume bottle" \
  --model gemini-3-pro-image-preview \
  --output output/perfume.png \
  --size 4K
```

Options:

- `--prompt, -p` — Text prompt (required)
- `--output, -o` — Output file path (default: `$XDG_CACHE_HOME/vertex-ai-images/generate-{ts}-{slug}.png`)
- `--model, -m` — Model ID (default: `gemini-3.1-flash-image-preview`)
- `--aspect-ratio, -a` — Aspect ratio: `1:1`, `1:4`, `1:8`, `2:3`, `3:2`, `3:4`, `4:1`, `4:3`, `4:5`, `5:4`, `8:1`, `9:16`, `16:9`, `21:9`
- `--size, -s` — Resolution: `512` (0.5K), `1K`, `2K`, `4K`
- `--image-only` — Return only image, suppress text output
- `--thinking-level, -t` — Thinking level: `minimal` (default) or `high`
- `--dry-run` — Preview without API call

### Edit an image

Provide one or more input images with a text instruction to modify them:

```bash
uv run --script scripts/vertex_ai_image.py edit \
  --prompt "Make the cat wear a top hat and monocle" \
  --image photo.jpg \
  --output output/fancy-cat.png
```

With multiple reference images (up to 14):

```bash
uv run --script scripts/vertex_ai_image.py edit \
  --prompt "Create a group photo of these people at a beach" \
  --image person1.png \
  --image person2.png \
  --image person3.png \
  --output output/group.png \
  --aspect-ratio 16:9 \
  --size 2K
```

Style transfer with a reference:

```bash
uv run --script scripts/vertex_ai_image.py edit \
  --prompt "Redraw this photo in watercolor style" \
  --image original.jpg \
  --output output/watercolor.png
```

Options:

- `--prompt, -p` — Edit instruction (required)
- `--image, -i` — Input image path or `gs://` URI (required, repeatable up to 14 times)
- `--output, -o` — Output file path (default: `$XDG_CACHE_HOME/vertex-ai-images/edit-{ts}-{slug}.png`)
- `--model, -m` — Model ID (default: `gemini-3.1-flash-image-preview`)
- `--aspect-ratio, -a` — Output aspect ratio
- `--size, -s` — Output resolution: `512`, `1K`, `2K`, `4K`
- `--image-only` — Return only image, suppress text output
- `--thinking-level, -t` — Thinking level: `minimal` or `high`
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
- `--model, -m` — Model ID (default: `gemini-2.5-flash`)
- `--dry-run` — Preview without API call

## Aspect Ratios & Resolutions

| Aspect Ratio | 512     | 1K        | 2K        | 4K        |
| ------------ | ------- | --------- | --------- | --------- |
| 1:1          | 512×512 | 1024×1024 | 2048×2048 | 4096×4096 |
| 16:9         | 688×384 | 1376×768  | 2752×1536 | 5504×3072 |
| 9:16         | 384×688 | 768×1376  | 1536×2752 | 3072×5504 |
| 3:2          | 632×424 | 1264×848  | 2528×1696 | 5056×3392 |
| 4:3          | 600×448 | 1200×896  | 2400×1792 | 4800×3584 |

> `512` resolution is only available on `gemini-3.1-flash-image-preview`.
> `gemini-2.5-flash-image` outputs 1024px only and does not support `--size`.

## Tips

- For text-heavy images (infographics, menus), generate the text first, then ask for an image containing it.
- Use `--thinking-level high` for complex compositions that need layout reasoning.
- Use `gemini-3-pro-image-preview` with `--size 4K` for professional-grade assets.
- Use `gemini-2.5-flash-image` for high-volume, low-latency batch workloads.
- Describe scenes narratively rather than listing keywords for best results.
