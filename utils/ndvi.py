import rasterio
import numpy as np
import matplotlib.pyplot as plt
import os

def calculate_ndvi(red_band, nir_band):
    return (nir_band - red_band) / (nir_band + red_band + 1e-6)

def process_and_save(red_path, nir_path):
    with rasterio.open(red_path) as red_src:
        red = red_src.read(1).astype('float32')
        profile = red_src.profile

    with rasterio.open(nir_path) as nir_src:
        nir = nir_src.read(1).astype('float32')

    ndvi = calculate_ndvi(red, nir)
    output_path = red_path.replace('.tif', '_ndvi.png')
    plt.imsave(output_path, ndvi, cmap='RdYlGn')
    return output_path
