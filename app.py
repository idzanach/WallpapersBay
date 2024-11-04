from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion import StableDiffusionPipeline
import torch
from PIL import Image
from io import BytesIO

app = Flask(__name__)

WALLPAPER_FOLDER = os.path.join(app.root_path, 'static', 'wallpapers')

model_id = "CompVis/stable-diffusion-v1-4"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
pipe = pipe.to("cpu")

@app.route('/')
def index():
    wallpapers = os.listdir(WALLPAPER_FOLDER)
    return render_template('index.html', wallpapers=wallpapers)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(WALLPAPER_FOLDER, filename, as_attachment=True, mimetype='image/png')

@app.route('/generate', methods=['POST'])
def generate():
    description = request.form.get("description")
    image = pipe(description, height=256, width=256, num_inference_steps=10).images[0]
    filename = f"{description.replace(' ', '_')}.png"
    filepath = os.path.join(WALLPAPER_FOLDER, filename)
    image.save(filepath)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

