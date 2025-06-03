import cv2
from PIL import Image, ImageTk

def convert_cv_to_tk(cv_img):
    img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    return ImageTk.PhotoImage(pil_img)