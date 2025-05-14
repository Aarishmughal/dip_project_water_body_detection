import cv2
import numpy as np
import os

def detect_water_and_contours(image_bgr, hsv_range):
    hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    
    lower_blue, upper_blue = hsv_range
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((5, 5), np.uint8)
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask_cleaned = cv2.morphologyEx(mask_cleaned, cv2.MORPH_CLOSE, kernel)

    water_pixel_count = cv2.countNonZero(mask_cleaned)
    total_pixels = mask_cleaned.shape[0] * mask_cleaned.shape[1]
    percentage = (water_pixel_count / total_pixels) * 100

    water_only = cv2.bitwise_and(image_bgr, image_bgr, mask=mask_cleaned)

    # Contour detection
    contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contoured_image = image_bgr.copy()
    cv2.drawContours(contoured_image, contours, -1, (0, 255, 0), 2)

    return water_only, contoured_image, water_pixel_count, percentage, mask_cleaned

def save_image(image, default_path="filtered_output.png"):
    cv2.imwrite(default_path, image)
    return os.path.abspath(default_path)