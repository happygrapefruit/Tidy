#!/usr/bin/env python3
"""tidy: sort the files in a folder into subfolders by type.

By default it only PREVIEWS what it would do. Pass --apply to actually move files.

    python tidy.py ~/Downloads            # preview
    python tidy.py ~/Downloads --apply    # do it
"""

import argparse
import shutil
import sys
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic", ".svg"},
    "Documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".pages"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".tsv", ".numbers"},
    "Presentations": {".ppt", ".pptx", ".key"},
    "Archives": {".zip", ".tar", ".gz", ".7z", ".rar"},
    "Audio": {".mp3", ".wav", ".m4a", ".flac"},
    "Video": {".mp4", ".mov", ".mkv", ".avi"},
    "Code": {".py", ".js", ".ts", ".html", ".css", ".json", ".ipynb"},
}


def category_for(path: Path) -> str:
    """Return the folder name a file belongs in, or 'Other'."""
    ext = path.suffix.lower()
    for name, extensions in CATEGORIES.items():
        if ext in extensions:
            return name
    return "Other"


def unique_destination(dest: Path) -> Path:
    """If dest already exists, add ' (1)', ' (2)', ... so nothing is overwritten."""
    if not dest.exists():
        return dest
    n = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({n}){dest.suffix}")
        if not candidate.exists():
            return candidate
        n += 1


def plan_moves(folder: Path) -> list[tuple[Path, Path]]:
    """List (source, destination) pairs for the files directly inside folder.

    Subfolders and hidden files (starting with '.') are left alone.
    """
    moves = []
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        dest = folder / category_for(item) / item.name
        moves.append((item, dest))
    return moves


def tidy(folder: Path, apply: bool = False) -> int:
    """Preview or perform the moves. Returns the number of files handled."""
    moves = plan_moves(folder)
    for source, dest in moves:
        if apply:
            dest.parent.mkdir(exist_ok=True)
            dest = unique_destination(dest)
            shutil.move(str(source), str(dest))
        print(f"{source.name}  ->  {dest.parent.name}/{dest.name}")
    return len(moves)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Sort files in a folder by type.")
    parser.add_argument("folder", type=Path, help="folder to tidy")
    parser.add_argument(
        "--apply", action="store_true", help="actually move files (default: preview only)"
    )
    args = parser.parse_args(argv)

    if not args.folder.is_dir():
        print(f"Not a folder: {args.folder}", file=sys.stderr)
        return 1

    count = tidy(args.folder, apply=args.apply)
    verb = "Moved" if args.apply else "Would move"
    print(f"\n{verb} {count} file(s)." + ("" if args.apply else " Re-run with --apply to do it."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
