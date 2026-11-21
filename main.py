#!/usr/bin/env python3
"""news-image-20261121 entrypoint.

Copies the pre-rendered front-page image (entry.png, in this repository)
to the grader's output directory as /output/entry.png.

Stdlib only, no network, no fonts, no randomness: every run writes the
same bytes. The image itself was drawn by render.py (same repository) from
five verified news stories of Saturday 21 November 2026; see README.md.
"""
import os
import shutil


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
