import ctypes, cv2, numpy as np
from pathlib import Path
import my_types as mt, compile

# compilando
path = "./core_c/image_processor.dll"
file = Path(path)
if not file.is_file():
    compile.compile_lib()

# importando dll e definindo funcs
ConvC = ctypes.CDLL(path)
ConvC.convoluteImg.argtypes = [
    ctypes.POINTER(mt.Img_h),
    ctypes.POINTER(mt.Matrix_h)
]
ConvC.defineMatrix.argtypes = [
    ctypes.POINTER(mt.Img_h),
    ctypes.POINTER(mt.Matrix_h)
]

# declarando handlers
kernel_h = mt.Matrix_h(
    filter = 0,
    size = 25
)
img_h = mt.Img_h()

# while pra pegar frames da webcam
cam = cv2.VideoCapture(0)
fps = cam.get(cv2.CAP_PROP_FPS)
print("FPS: ", fps)

while True:
    ret, frame = cam.read()
    if not ret:
        break
    img_h.data = frame.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    img_h.h, img_h.w, img_h.c = frame.shape

    ConvC.defineMatrix(ctypes.byref(img_h), ctypes.byref(kernel_h))
    ConvC.convoluteImg(ctypes.byref(img_h), ctypes.byref(kernel_h))
    new_frame = np.ctypeslib.as_array(img_h.data, shape=frame.shape)

    cv2.imshow("Webcam", new_frame)
    key = cv2.waitKey(2)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()