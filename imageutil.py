#!/usr/bin/env python3

import ctypes

imageutil = ctypes.cdll.LoadLibrary("./imageutil/bin/libimageutil.so")

imageutil.load_image.restype = ctypes.POINTER(ctypes.c_uint8)
imageutil.load_image.argtypes = (
    ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32), ctypes.c_int32)

imageutil.load_imagef.restype = ctypes.POINTER(ctypes.c_float)
imageutil.load_imagef.argtypes = (
    ctypes.c_char_p, ctypes.POINTER(ctypes.c_int32), ctypes.POINTER(ctypes.c_int32), ctypes.c_int32)

imageutil.free_image.restype = None
imageutil.free_image.argtypes = (ctypes.c_void_p,)

imageutil.resize_image.restype = ctypes.c_int32
imageutil.resize_image.argtypes = (
    ctypes.POINTER(ctypes.c_uint8), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,
    ctypes.POINTER(ctypes.c_uint8), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,
    ctypes.c_int32)

imageutil.resize_imagef.restype = ctypes.c_int32
imageutil.resize_imagef.argtypes = (
    ctypes.POINTER(ctypes.c_float), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,
    ctypes.POINTER(ctypes.c_float), ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,
    ctypes.c_int32)
