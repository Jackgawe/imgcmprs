import argparse
import os
from PIL import Image
import sys
import traceback
import shutil
# ohhhhhhhh and now for our amazing show, "How horrible the code can get" brought to you by: :drumroll: Chris hansen
def get_save_format(ext):
    ext = ext.lstrip('.')
    if ext in ('jpg', 'jpeg'):
        return 'JPEG'
    if ext == 'png':
        return 'PNG'
    return None

def compress_image(input_path, output_path, quality, lossless, debug, force):
    try:
        img = Image.open(input_path)
        ext = os.path.splitext(input_path)[1].lower()
        in_place = os.path.abspath(input_path) == os.path.abspath(output_path)
        save_format = get_save_format(ext)
        comp_path = None
        if save_format is None:
            print(f"[ERROR] Unsupported file extension for '{input_path}'. Only JPEG and PNG are allowed.")
            return False

        # For in-place: always save as _comp, never overwrite original
        if in_place:
            base, ext_base = os.path.splitext(input_path)
            comp_path = f"{base}_comp{ext_base}"
            real_output = comp_path
        else:
            real_output = output_path

        if debug:
            print(f"[DEBUG] Processing: {input_path}")
            print(f"[DEBUG] Format: {ext}, Output: {output_path}")
            print(f"[DEBUG] Options: quality={quality}, lossless={lossless}, in_place={in_place}, force={force}")
            print(f"[DEBUG] Compressed will be at: {real_output}")
        save_kwargs = {'format': save_format}
        if lossless:
            if ext in (".png",):
                img.save(real_output, optimize=True, **save_kwargs)
            elif ext in (".jpg", ".jpeg"):
                img.save(real_output, quality=100, optimize=True, progressive=True, **save_kwargs)
            else:
                img.save(real_output, **save_kwargs)
        else:
            if ext in (".jpg", ".jpeg"):
                img.save(real_output, optimize=True, quality=quality, **save_kwargs)
            elif ext == ".png":
                img.save(real_output, optimize=True, **save_kwargs)
            else:
                img.save(real_output, **save_kwargs)
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(real_output)
        if debug:
            print(f"[DEBUG] Input size: {original_size} bytes ; Output size: {compressed_size} bytes")
        if compressed_size < original_size or force:
            print(f"Compressed: {input_path} -> {real_output} [{original_size//1024}KB → {compressed_size//1024}KB]")
            return (input_path, real_output)
        else:
            print(f"Warning: {real_output} is larger than or equal to original! Keeping original. [{original_size//1024}KB → {compressed_size//1024}KB]")
            if os.path.exists(real_output):
                os.remove(real_output)
            return False
    except Exception as e:
        print(f"Failed to compress {input_path}: {e}")
        if debug:
            traceback.print_exc()
        if comp_path and os.path.exists(comp_path):
            os.remove(comp_path)
        return False

def process_folder(input_folder, output_folder, quality, recursive, lossless, debug, force):
    changed_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith((".jpg", ".jpeg", ".png")):
                in_path = os.path.join(root, file)
                rel_path = os.path.relpath(in_path, input_folder)
                out_path = os.path.join(output_folder, rel_path)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                result = compress_image(in_path, out_path, quality, lossless, debug, force)
                if result:
                    changed_files.append(result)
        if not recursive:
            break
    return changed_files

def ask_delete_or_keep_copy(targets, force, debug):
    if force:
        print("[INFO] Force flag set; skipping delete prompts. Originals kept.")
        return
    if len(targets) == 1:
        original, compressed = targets[0]
        # in-place means _comp file exists and original remains
        answer = input(f"Do you want to delete the original file after compression? [y/N] ").strip().lower()
        if answer == 'y':
            try:
                os.remove(original)
                print(f'Original file deleted: {original}')
            except Exception as e:
                print(f'Failed to delete original: {e}')
        else:
            print('Both files kept.')
    else:
        answer = input(f"Do you want to delete the original file(s) after compression? [y/N] ").strip().lower()
        if answer == 'y':
            for original, compressed in targets:
                try:
                    os.remove(original)
                    print(f"Deleted: {original}")
                except Exception as e:
                    print(f"Could not delete {original}: {e}")
        else:
            print('Original file(s) kept (batch mode).')

def main():
    parser = argparse.ArgumentParser(
        description="Image Compressor CLI Tool: Lossless/lossy JPEG and PNG compression.\n\nFlags:\n  -i   Input file or folder (required)\n  -o   Output file or folder (optional)\n  -q   JPEG quality, 1-95 (default 60, ignored in lossless mode)\n  -l   Use lossless compression for PNG/JPEG\n  -r   Recursively process folders\n  -d   Enable debug output\n  -f   Force overwrite even if output is bigger\n  -info   Show tool info and exit",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # a bunch of crap, its just the flags
    parser.add_argument('-i', metavar='PATH', help='Input file or folder (required)')
    parser.add_argument('-o', metavar='PATH', help='Output file or folder (optional)')
    parser.add_argument('-q', type=int, default=60, metavar='N', help='JPEG quality, 1-95 (default 60, ignored with -l)')
    parser.add_argument('-l', action='store_true', help='Lossless compression for PNG/JPEG (flag)')
    parser.add_argument('-r', action='store_true', help='Recursively process folders (flag)')
    parser.add_argument('-d', action='store_true', help='Enable debug output (flag)')
    parser.add_argument('-f', action='store_true', help='Force overwrite even if output is bigger (flag)')
    parser.add_argument('-info', action='store_true', help='Show tool info and exit')
    args = parser.parse_args()

    if args.info:
        print("imgcmprs: Fast, safe CLI to compress JPEG & PNG (lossless/lossy, batch/single)\nVersion: 0.1.1\nAuthor: Eyad Mohammed\nDescription: Compress images with lossless/lossy options as a simple CLI. Supports in-place and batch mode.\nProject: https://github.com/jackgawe/imgcmprs")
        sys.exit(0)

    if not args.i:
        parser.error("the following arguments are required: -i")

    input_path = args.i
    output_path = args.o
    quality = args.q
    recursive = args.r
    lossless = args.l
    debug = args.d
    force = args.f

    changed_files = []
    if os.path.isfile(input_path):
        out = output_path if output_path else input_path
        result = compress_image(input_path, out, quality, lossless, debug, force)
        if result:
            changed_files.append(result)
    elif os.path.isdir(input_path):
        out = output_path if output_path else input_path + "_compressed"
        os.makedirs(out, exist_ok=True)
        changed_files = process_folder(input_path, out, quality, recursive, lossless, debug, force)
    else:
        print("Input path is not a valid file or directory.")
        sys.exit(1)

    if changed_files:
        ask_delete_or_keep_copy(changed_files, force, debug)

if __name__ == "__main__":
    main()
