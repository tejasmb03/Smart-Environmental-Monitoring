from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from utils import enchroach, ground, ndvi, satellite
import matplotlib.pyplot as plt
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enchroach', methods=['GET', 'POST'])
def enchroach_view():
    result = None
    if request.method == 'POST':
        img1 = request.files['image1']
        img2 = request.files['image2']
        path1 = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4().hex}_{img1.filename}")
        path2 = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4().hex}_{img2.filename}")
        img1.save(path1)
        img2.save(path2)

        contours1, wbi1, area1, percent1 = enchroach.process_image(path1)
        contours2, wbi2, area2, percent2 = enchroach.process_image(path2)

        out1 = path1.replace('.jpg', '_out1.png')
        out2 = path2.replace('.jpg', '_out2.png')
        plt.imsave(out1, contours1)
        plt.imsave(out2, contours2)
        result = (out1, out2, percent1, percent2)

    return render_template('enchroach.html', result=result)

@app.route('/ground')
def ground_view():
    images = ground.load_images()
    return render_template('ground.html', results=images)

@app.route('/satellite')
def satellite_view():
    results = satellite.load_and_process()
    return render_template('satellite.html', results=results)

@app.route('/ndvi', methods=['GET', 'POST'])
def ndvi_view():
    image_path = None
    if request.method == 'POST':
        red = request.files['red_band']
        nir = request.files['nir_band']
        red_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4().hex}_{red.filename}")
        nir_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4().hex}_{nir.filename}")
        red.save(red_path)
        nir.save(nir_path)

        ndvi_img_path = ndvi.process_and_save(red_path, nir_path)
        image_path = ndvi_img_path

    return render_template('ndvi.html', image=image_path)

@app.route('/urbanvisualize')
def urban_visualize_view():
    return render_template('urbanvisualize.html')



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
