import ctypes, cv2, numpy as np, time
from pathlib import Path
import my_types as mt, compile

filters = ["ColorShift", "NegativeColor", "GreyScale", "SobelEdge", "LaplacianEdge", "Emboss", "Identity", "Blur", "Uniform", "MotionBlur", "Sharpen"]

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
    filter = 6,
    size = 15
)
img_h = mt.Img_h()

# while pra pegar frames da webcam
cam = cv2.VideoCapture(0)
fps_default = cam.get(cv2.CAP_PROP_FPS)
print("FPS padrão: ", fps_default)

while True:
    ret, frame = cam.read()
    if not ret:
        break
    start = time.perf_counter()

    img_h.data = frame.ctypes.data_as(ctypes.POINTER(ctypes.c_ubyte))
    img_h.h, img_h.w, img_h.c = frame.shape

    ConvC.defineMatrix(ctypes.byref(img_h), ctypes.byref(kernel_h))
    ConvC.convoluteImg(ctypes.byref(img_h), ctypes.byref(kernel_h))
    new_frame = np.ctypeslib.as_array(img_h.data, shape=frame.shape)

    end = time.perf_counter()
    fps = 1 // (end - start)
    texto = f"FPS máximo: {min(fps, fps_default)} - {filters[kernel_h.filter]}"
    cv2.putText(new_frame, texto, (50, 50), cv2.FONT_HERSHEY_PLAIN, 0.8, (0, 0, 255), 1)

    cv2.imshow(f"Webcam", new_frame)

    key = cv2.waitKeyEx(1)
    if key in [2490368, 65362]: # top
        if kernel_h.size <= 45:
            kernel_h.size += 5

    elif key in [2621440, 65364]: # down
        if kernel_h.size >= 5:
            kernel_h.size -= 5

    elif key in [2424832, 65361]: # left
        if kernel_h.filter >= 1:
            kernel_h.filter -= 1

    elif key in [2555904, 65363]: # right
        if kernel_h.filter <= 9:
            kernel_h.filter += 1

    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()