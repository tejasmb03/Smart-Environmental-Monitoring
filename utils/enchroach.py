import cv2
import numpy as np

def process_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise Exception(f"Image not found at {image_path}")

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([140, 255, 255])
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    kernel = np.ones((5, 5), np.uint8)
    blue_mask_cleaned = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(blue_mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    image_with_contours = image_rgb.copy()
    cv2.drawContours(image_with_contours, contours, -1, (255, 0, 0), 2)

    blue_channel = image_rgb[:, :, 2].astype(float)
    green_channel = image_rgb[:, :, 1].astype(float)
    wbi = (blue_channel - green_channel) / (blue_channel + green_channel + 1e-6)
    wbi_normalized = cv2.normalize(wbi, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    wbi_colormap = cv2.applyColorMap(wbi_normalized, cv2.COLORMAP_JET)

    total_water_area = np.sum(blue_mask_cleaned == 255)
    total_pixels = blue_mask_cleaned.size
    percentage_water = (total_water_area / total_pixels) * 100

    return image_with_contours, wbi_colormap, total_water_area, percentage_water
