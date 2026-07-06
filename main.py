import ctypes, cv2
from pathlib import Path
import my_types, compile

path = "./core_c/filtro.dll"
file = Path(path)
if not file.is_file():
    compile.compile_lib()

ConvC = ctypes.CDLL(path)
ConvC.convoluteImg.argtypes = [
    ctypes.POINTER(my_types.ImgH),
    ctypes.POINTER(my_types.MatrixH)
]

cam = cv2.VideoCapture(0)
_, frame = cam.read()
width, height, channels = frame.shape
print(frame)

while True:
    break
    _, frame = cam.read()
    if not ret:
        break
    cv2.imshow("Webcam", frame)
    key = cv2.waitKey(1000)
    if key == 27:
        break

cam.release()
cv2.destroyAllWindows()