import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

def process_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2HSV)

    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    kernel = np.ones((5, 5), np.uint8)
    mask_cleaned = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(mask_cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_image = image_rgb.copy()
    cv2.drawContours(contour_image, contours, -1, (255, 0, 0), 2)

    output_img_path = image_path.replace('.jpg', '_result.png')
    plt.imsave(output_img_path, contour_image)

    total_area = np.sum(mask_cleaned == 255)
    percent = (total_area / mask_cleaned.size) * 100

    return output_img_path, total_area, percent

def load_and_process():
    folder = 'static/uploads/satellite'  # Add satellite images here
    results = {}
    for year in range(2016, 2025):
        path = os.path.join(folder, f"{year}.jpg")
        if os.path.exists(path):
            try:
                image_path, area, percent = process_image(path)
                results[year] = {'image_path': image_path, 'area': area, 'percent': percent}
            except Exception as e:
                print(f"Error for year {year}: {e}")
    return results
