#!/usr/bin/env python3

import os
import sys
import ctypes
from imageutil import imageutil
from argparse import ArgumentParser

DEFAULT_WIDTH = 80
DEFAULT_TONE = " .,:;i1tfLCG08@"

def get_brightness(r, g, b):
    return r * 0.299 + g * 0.587 + b * 0.114  # ITU-R Rec. BT.601

def output_image(args, data, value_max, width, height, channels):
    assert(channels == 3 or channels == 4)

    tone = args.tone
    index = 0
    if args.frame:
        print("-" * (width + 2))
    for y in range(0, height):
        row = ""
        for x in range(0, width):
            r = max(0, min(data[index + 0], value_max)) / value_max
            g = max(0, min(data[index + 1], value_max)) / value_max
            b = max(0, min(data[index + 2], value_max)) / value_max
            brightness = get_brightness(r, g, b)
            row += tone[min(int(brightness * len(tone)), len(tone) - 1)]
            index += channels
        if args.frame:
            row = "-" + row + "-"
        print(row)
    if args.frame:
        print("-" * (width + 2))

def main(argv):
    ap = ArgumentParser(add_help=False)
    ap.add_argument("filename")
    ap.add_argument("-w", "--width", default=0)
    ap.add_argument("-h", "--height", default=0)
    ap.add_argument("-f", "--frame", action="store_true")
    ap.add_argument("-t", "--tone", type=str, default=DEFAULT_TONE)
    ap.add_argument("-i", "--invert", action="store_true")
    args = ap.parse_args(argv[1:])

    if args.invert:
        args.tone = args.tone[::-1]

    if not os.path.exists(args.filename):
        print(f"{args.filename}: No such file", file=sys.stderr)
        return 1

    c_filename = args.filename.encode("utf-8")
    c_width = ctypes.c_int32()
    c_height = ctypes.c_int32()
    c_data = ctypes.POINTER(ctypes.c_uint8)
    channels = 3

    c_data = imageutil.load_image(c_filename, c_width, c_height, channels)

    resized_width = max(0, int(args.width))
    resized_height = max(0, int(args.height))
    if resized_width == 0 and resized_height == 0:
        resized_width = min(c_width.value, DEFAULT_WIDTH)

    if resized_width == 0:
        resized_width = max(1, int(resized_height * c_width.value / (c_height.value / 2)))
    elif resized_height == 0:
        resized_height = max(1, int(resized_width * (c_height.value / 2) / c_width.value))
    else:
        pass

    c_resized_data = (ctypes.c_uint8 * (channels * resized_width * resized_height))()
    imageutil.resize_image(
        c_data, c_width.value, c_height.value, 0,
        c_resized_data, resized_width, resized_height, 0,
        channels)
    imageutil.free_image(c_data)

    output_image(args, c_resized_data, 255, resized_width, resized_height, channels)

    return 0

if __name__ == "__main__":
    main(sys.argv)
