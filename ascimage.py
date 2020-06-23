#!/usr/bin/env python3

import os
import sys
import ctypes
from imageutil import Image
from argparse import ArgumentParser

DEFAULT_WIDTH = 80
DEFAULT_TONE = " .,:;i1tfLCG08@"

def get_brightness(r, g, b):
    return r * 0.299 + g * 0.587 + b * 0.114  # ITU-R Rec. BT.601

def output_image(args, image):
    assert(image.channels == 3 or image.channels == 4)

    tone = args.tone
    index = 0
    vmin, vmax = image.value_range
    if args.frame:
        print("-" * (image.width + 2))
    for y in range(0, image.height):
        row = ""
        for x in range(0, image.width):
            a = max(vmin, min(image.data[index + 3], vmax)) / vmax if (image.channels == 4) else 1
            r = max(vmin, min(image.data[index + 0], vmax)) / vmax * a
            g = max(vmin, min(image.data[index + 1], vmax)) / vmax * a
            b = max(vmin, min(image.data[index + 2], vmax)) / vmax * a
            brightness = get_brightness(r, g, b)
            row += tone[min(int(brightness * len(tone)), len(tone) - 1)]
            index += image.channels
        if args.frame:
            row = "-" + row + "-"
        print(row)
    if args.frame:
        print("-" * (image.width + 2))

def main(argv):
    ap = ArgumentParser(add_help=False)
    ap.add_argument("filename")
    ap.add_argument("-w", "--width", default=0)
    ap.add_argument("-h", "--height", default=0)
    ap.add_argument("-f", "--frame", action="store_true")
    ap.add_argument("-t", "--tone", type=str, default=DEFAULT_TONE)
    ap.add_argument("-i", "--invert", action="store_true")
    args = ap.parse_args(argv[1:])

    if not os.path.exists(args.filename):
        print(f"{args.filename}: No such file", file=sys.stderr)
        return 1

    if args.invert:
        args.tone = args.tone[::-1]

    image = Image.load(args.filename, channels=4)

    resized_width = max(0, int(args.width))
    resized_height = max(0, int(args.height))
    if resized_width == 0 and resized_height == 0:
        resized_width = min(image.width, DEFAULT_WIDTH)

    if resized_width == 0:
        resized_width = max(1, int((resized_height * image.width / image.height / 2)))
    elif resized_height == 0:
        resized_height = max(1, int((resized_width * image.height / 2) / image.width))
    else:
        pass

    resized_image = image.get_resized(resized_width, resized_height)
    output_image(args, resized_image)

    return 0

if __name__ == "__main__":
    main(sys.argv)
