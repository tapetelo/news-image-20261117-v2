#!/usr/bin/env python3
"""Entry 2 for news-image-20261117: hand over the finished picture.

The picture itself was composed beforehand (see render.py): the
user-supplied nine-story grid, a navy masthead, and a ticker of
verified 17 November 2026 news, all baked into entry.png next to
this file. The grader's sandbox installs nothing, so this program
sticks to the standard library and does one job only: place that
finished picture where the grader expects it.

Note on the file: entry.png carries JPEG bytes. The kit allows a
PNG or a JPEG, told apart by its first bytes, with the name staying
entry.png — a PNG of this photographic grid ran over the 1 MiB gate.
"""
import os
import shutil
import sys

IMAGE_NAME = "entry.png"


def locate_image():
    """Return the path of the bundled picture beside this program."""
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, IMAGE_NAME)


def run():
    picture = locate_image()
    if not os.path.isfile(picture):
        print(f"{IMAGE_NAME} is missing beside {__file__}", file=sys.stderr)
        return 1
    destination_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "./out"
    os.makedirs(destination_dir, exist_ok=True)
    destination = os.path.join(destination_dir, IMAGE_NAME)
    shutil.copyfile(picture, destination)
    print(f"wrote {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(run())
