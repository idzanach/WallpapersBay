from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__)

WALLPAPER_FOLDER = os.path.join(app.root_path, 'static', 'wallpapers')

@app.route('/')
def index():
    wallpapers = os.listdir(WALLPAPER_FOLDER)
    return render_template('index.html', wallpapers=wallpapers)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(WALLPAPER_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
