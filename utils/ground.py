import os
import cv2

def read_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

def load_images():
    folder = 'static/uploads/ground'  # Put your ground images here
    results = {}
    for year in range(2016, 2025):
        path = os.path.join(folder, f"{year}.png")
        if os.path.exists(path):
            results[year] = path
    return results
