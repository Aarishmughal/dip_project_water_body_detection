import tkinter as tk
from tkinter import filedialog, Label, Button, Scale, HORIZONTAL, Frame
import cv2
import numpy as np
import matplotlib.pyplot as plt
from processing import detect_water_and_contours, save_image
from utils import convert_cv_to_tk

class WaterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Body Detection")
        self.root.geometry("1800x800")
        self.root.configure(bg='#f0f0f0')

        self.image = None
        self.water_only = None
        self.contour_image = None
        self.mask = None

        tk.Label(root, text="Water Body Detector", font=("Arial", 24, "bold"), bg='#f0f0f0').pack(pady=10)

        top_frame = Frame(root, bg='#f0f0f0')
        top_frame.pack(pady=10)

        self.panel_orig = Label(top_frame)
        self.panel_orig.pack(side="left", padx=10)

        self.panel_result = Label(top_frame)
        self.panel_result.pack(side="left", padx=10)

        self.info_label = Label(root, text="", font=("Arial", 14), bg='#f0f0f0')
        self.info_label.pack(pady=10)

        Button(root, text="Upload Image", font=("Arial", 14), command=self.load_image, bg="#2e8b57", fg="white").pack(pady=5)
        Button(root, text="Save Result", font=("Arial", 14), command=self.save_result, bg="#4682b4", fg="white").pack(pady=5)
        Button(root, text="Show Histogram", font=("Arial", 14), command=self.show_histogram, bg="#6a5acd", fg="white").pack(pady=5)
        Button(root, text="Edge Detection", font=("Arial", 14), command=self.show_edges, bg="#ff6347", fg="white").pack(pady=5)
        Button(root, text="Show Pixel Stats", font=("Arial", 14), command=self.show_pixel_stats, bg="#daa520", fg="white").pack(pady=5)

        self.slider_frame = Frame(root, bg='#f0f0f0')
        self.slider_frame.pack(pady=10)

        self.sliders = {}
        for i, (label, from_, to_, init) in enumerate([
            ("H Min", 0, 179, 85),
            ("H Max", 0, 179, 135),
            ("S Min", 0, 255, 30),
            ("S Max", 0, 255, 255),
            ("V Min", 0, 255, 20),
            ("V Max", 0, 255, 255)
        ]):
            l = Label(self.slider_frame, text=label, font=("Arial", 10), bg='#f0f0f0')
            l.grid(row=0, column=i, padx=5)
            s = Scale(self.slider_frame, from_=from_, to=to_, orient=HORIZONTAL, command=self.update_sliders)
            s.set(init)
            s.grid(row=1, column=i, padx=5)
            self.sliders[label] = s
        # self.show_pixel_stats()

    def load_image(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        self.image = cv2.imread(path)
        self.image = cv2.resize(self.image, (800, 600))
        self.update_detection()

    def update_sliders(self, _=None):
        if self.image is not None:
            self.update_detection()

    def update_detection(self):
        lower_blue = np.array([
            self.sliders["H Min"].get(),
            self.sliders["S Min"].get(),
            self.sliders["V Min"].get()
        ])
        upper_blue = np.array([
            self.sliders["H Max"].get(),
            self.sliders["S Max"].get(),
            self.sliders["V Max"].get()
        ])

        self.water_only, self.contour_image, water_pixels, percentage, self.mask = detect_water_and_contours(self.image, (lower_blue, upper_blue))

        img_orig = convert_cv_to_tk(self.image)
        img_result = convert_cv_to_tk(self.contour_image)

        self.panel_orig.configure(image=img_orig)
        self.panel_orig.image = img_orig

        self.panel_result.configure(image=img_result)
        self.panel_result.image = img_result

        self.info_label.config(text=f"Water Pixels: {water_pixels} | Water Coverage: {percentage:.2f}%")

    def save_result(self):
        if self.water_only is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                save_image(self.water_only, file_path)

    def show_histogram(self):
        if self.mask is not None:
            plt.figure("Histogram of Detected Water Mask")
            plt.hist(self.mask.ravel(), bins=256, range=(0, 256), color='blue')
            plt.title("Histogram of Water Mask")
            plt.xlabel("Pixel Intensity")
            plt.ylabel("Frequency")
            plt.grid(True)
            plt.show()

    def show_edges(self):
        if self.water_only is not None:
            edges = cv2.Canny(self.water_only, 100, 200)
            img_edges = convert_cv_to_tk(edges)
            self.panel_result.configure(image=img_edges)
            self.panel_result.image = img_edges

    def show_pixel_stats(self):
        if self.mask is not None:
            water_pixels = cv2.countNonZero(self.mask)
            total_pixels = self.mask.shape[0] * self.mask.shape[1]
            percentage = (water_pixels / total_pixels) * 100
            stats_text = f"Water Pixels: {water_pixels} | Total Pixels: {total_pixels} | Coverage: {percentage:.2f}%"
            self.info_label.config(text=stats_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = WaterApp(root)
    root.mainloop()
