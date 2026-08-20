#!/usr/bin/env python3
##########################################################################
#
# pgAdmin Website
#
# Copyright (C) 2017, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

"""Build the gallery thumbnails for the features page.

The screenshots in static/img/screenshots are around 2796x2198 and 4.3MB in
total. The gallery used to point its <img> tags straight at them, so opening
the page downloaded every full size screenshot to render a grid of tiles a
couple of hundred pixels wide. These thumbnails come to half a megabyte.

Each one is cropped to the tile's aspect ratio from the top left before being
scaled, rather than letterboxed: a whole 4:3 application window shrunk to a
240x150 tile is an unreadable grey smudge, whereas the top left corner shows
the menu, the browser tree and enough of the active panel to tell the
screenshots apart.

Run it after adding or replacing anything in static/img/screenshots:

    ~/venv/django52/bin/python tools/make-screenshot-thumbs.py

Requires Pillow. The output is committed, so this only needs running when the
sources change.
"""

import argparse
import glob
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit('Pillow is required: pip install Pillow')


# Twice the width the grid renders a tile at, so they stay sharp on a high
# density display.
TARGET_WIDTH = 800

# Tile aspect ratio. Must match --gallery-tile-ratio in _gallery.scss.
RATIO = 16 / 10

SOURCE_DIR = os.path.join('static', 'img', 'screenshots')
OUTPUT_DIR = os.path.join(SOURCE_DIR, 'thumbs')


def build(source_dir, output_dir, quiet=False):
    os.makedirs(output_dir, exist_ok=True)

    sources = sorted(glob.glob(os.path.join(source_dir, '*.png')))
    if not sources:
        sys.exit('No screenshots found in %s' % source_dir)

    bytes_in = bytes_out = 0

    for path in sources:
        name = os.path.basename(path)
        dest = os.path.join(output_dir, os.path.splitext(name)[0] + '.webp')

        # RGBA first, then RGB: some of these are palette images carrying
        # transparency, which Pillow warns about if converted directly.
        image = Image.open(path).convert('RGBA').convert('RGB')
        bytes_in += os.path.getsize(path)

        width, height = image.size
        wanted_height = int(width / RATIO)
        if wanted_height < height:
            image = image.crop((0, 0, width, wanted_height))
        else:
            image = image.crop((0, 0, int(height * RATIO), height))

        image = image.resize(
            (TARGET_WIDTH, int(TARGET_WIDTH / RATIO)), Image.LANCZOS)
        image.save(dest, 'WEBP', quality=82, method=6)
        bytes_out += os.path.getsize(dest)

        if not quiet:
            print('  %s' % os.path.basename(dest))

    print('%d thumbnails: %.1f MB of sources became %.1f MB'
          % (len(sources), bytes_in / 1048576, bytes_out / 1048576))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default=SOURCE_DIR,
                        help='directory of full size screenshots')
    parser.add_argument('--output', default=OUTPUT_DIR,
                        help='directory to write thumbnails to')
    parser.add_argument('--quiet', action='store_true',
                        help='only print the summary')
    args = parser.parse_args()

    build(args.source, args.output, args.quiet)


if __name__ == '__main__':
    main()
