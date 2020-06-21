#!/usr/bin/env python3

import ctypes

imageutil = ctypes.cdll.LoadLibrary("./imageutil/bin/libimageutil.so")

imageutil.load_image.restype = ctypes.POINTER(ctypes.c_uint8)
imageutil.load_image.argtypes = (
    ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32), ctypes.c_int32)

imageutil.free_image.restype = None
imageutil.free_image.argtypes = (ctypes.c_void_p,)

imageutil.resize_image.restype = ctypes.c_int32
imageutil.resize_image.argtypes = (
    ctypes.POINTER(ctypes.c_uint8), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,
    ctypes.POINTER(ctypes.c_uint8), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,
    ctypes.c_int32)

class Image(object):
    def __init__(self):
        self.data = None
        self.width = 0
        self.height = 0
        self.channels = 0
        self.value_range = (0, 0)

    @classmethod
    def load(cls, filename, channels):
        image = Image()
        c_filename = filename.encode("utf-8")
        c_width = ctypes.c_int32()
        c_height = ctypes.c_int32()
        data = imageutil.load_image(c_filename, c_width, c_height, channels)
        data_count = int(channels * c_width.value * c_height.value)
        image.data = (ctypes.c_uint8 * data_count)()
        ctypes.memmove(image.data, data, data_count)
        imageutil.free_image(data)
        image.width = c_width.value
        image.height = c_height.value
        image.channels = channels
        image.value_range = (0, 255)
        return image

    def get_resized(self, resized_width, resized_height, resized_channels=None):
        if not self.data:
            return None
        resized_channels = resized_channels or self.channels
        resized_image = Image()
        resized_image.width = int(resized_width)
        resized_image.height = int(resized_height)
        resized_image.channels = int(resized_channels)
        data_count = int(resized_image.channels * resized_image.width * resized_image.height)
        resized_image.data = (ctypes.c_uint8 * data_count)()
        resized_image.value_range = self.value_range
        result = imageutil.resize_image(
            self.data, self.width, self.height, 0,
            resized_image.data, resized_image.width, resized_image.height, 0,
            resized_image.channels
            )
        return resized_image if (result == 1) else None
