import argparse
import os
from PIL import Image

def compress_image(input_path, output_path, quality, lossless):
    try:
        img = Image.open(input_path)
        ext = os.path.splitext(input_path)[1].lower()
        if lossless:
            if ext in (".png",):
                img.save(output_path, optimize=True)
            elif ext in (".jpg", ".jpeg"):
                img.save(output_path, quality=100, optimize=True, progressive=True)
            else:
                img.save(output_path)
        else:
            if ext in (".jpg", ".jpeg"):
                img.save(output_path, optimize=True, quality=quality)
            elif ext == ".png":
                img.save(output_path, optimize=True)
            else:
                img.save(output_path)
        print(f"Compressed: {input_path} -> {output_path}")
    except Exception as e:
        print(f"Failed to compress {input_path}: {e}")

def process_folder(input_folder, output_folder, quality, recursive, lossless):
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                in_path = os.path.join(root, file)
                rel_path = os.path.relpath(in_path, input_folder)
                out_path = os.path.join(output_folder, rel_path)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                compress_image(in_path, out_path, quality, lossless)
        if not recursive:
            break

def main():
    parser = argparse.ArgumentParser(description="Image Compressor CLI Tool")
    parser.add_argument('--input', '-i', required=True, help='Input file or folder')
    parser.add_argument('--output', '-o', help='Output file or folder (optional)')
    parser.add_argument('--quality', '-q', type=int, default=60, help='Compression quality (1-95, default 60; ignored if --lossless)')
    parser.add_argument('--recursive', '-r', action='store_true', help='Recursively process folders')
    parser.add_argument('--lossless', '-l', action='store_true', help='Use lossless compression (only for PNG/JPEG)')
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    quality = args.quality
    recursive = args.recursive
    lossless = args.lossless

    if os.path.isfile(input_path):
        out = output_path if output_path else input_path
        compress_image(input_path, out, quality, lossless)
    elif os.path.isdir(input_path):
        out = output_path if output_path else input_path + "_compressed"
        os.makedirs(out, exist_ok=True)
        process_folder(input_path, out, quality, recursive, lossless)
    else:
        print("Input path is not a valid file or directory.")

if __name__ == "__main__":
    main()
