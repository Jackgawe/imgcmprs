# imgcmprs

A fast, easy-to-use Python CLI tool for compressing JPEG and PNG images with both lossless and lossy modes.

---

## Features
- Compresses images individually or in bulk (folders)
- Supports JPEG and PNG
- **Lossless mode** (`--lossless`): Optimizes files without visible quality loss
- **Lossy mode** (`--quality`): Reduce file size by lowering image quality
- Recursive directory support
- Custom output folder
- Cross-platform, requires Python 3.7+

---

## Installation

1. Install Python 3.7+
2. Clone this repo and install:
   ```bash
   pip install -e .
   # Or for user-local install:
   pip install --user .
   ```

---

## Usage

### Compress a single image (lossy, 60% quality):

```bash
imgcmprs --input myphoto.jpg --quality 60
```

### Compress a folder (lossless, best for PNG):

```bash
imgcmprs --input images/ --output optimized/ --lossless --recursive
```

### Options
- `--input, -i`     Input file or directory (required)
- `--output, -o`    Output file or directory (optional)
- `--quality, -q`   JPEG quality (default: 60, ignored in lossless mode)
- `--lossless, -l`  Use lossless compression (recommended for PNG)
- `--recursive, -r` Recursively compress directories

---

## Requirements
- Python 3.7+
- Pillow (`pip install Pillow`)

---

## Notes
- Lossless for PNG is truly lossless; for JPEG, uses `quality=100` with optimizations (minor effect but no further visual loss).
- Output defaults to `_compressed` directory if not specified for folders.
- Re-run with `--lossless` to optimize previously compressed images further (if possible).

---

## License
MIT
