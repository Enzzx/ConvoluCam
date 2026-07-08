import ctypes
from enum import IntEnum

if __name__ == "__main__":
    print("aqui nao man")
    exit()

class Filter_type(IntEnum):
    ColorShift = 0
    NegativeColor = 1
    GreyScale = 2

    SobelEdge = 3
    LaplacianEdge = 4
    Emboss = 5
    Identity = 6

    Blur = 7
    Uniform = 8
    MotionBlur = 9
    Sharpen = 10

class Img_h(ctypes.Structure):
    _fields_ = [
        ("w", ctypes.c_int),
        ("h", ctypes.c_int),
        ("c", ctypes.c_int),
        ("pS", ctypes.c_int),
        ("kt", ctypes.c_int),
        ("data", ctypes.POINTER(ctypes.c_ubyte))
    ]

class Matrix_h(ctypes.Structure):
    _fields_ = [
        ("M", ctypes.POINTER(ctypes.c_float)),
        ("size", ctypes.c_int),
        ("filter", ctypes.c_int)
    ]