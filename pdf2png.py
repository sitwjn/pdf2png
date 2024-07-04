"""
MIT License

Copyright (c) 2024 Jianai Wang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from flask import Flask, request, send_file, jsonify, Response
from werkzeug.utils import secure_filename
import sys
import io
import os
import pdfplumber
import zipfile
import markdown as md
from waitress import serve

app = Flask(__name__)

home_path = ''

if len(sys.argv) > 1:
    home_path = sys.argv[1]

def get_im_bytes(file_obj, file_name, resolution):
    im_bytes = []
    with pdfplumber.open(file_obj) as pdf:
        file_name = file_name + '-%s.png'
        for i, page in enumerate(pdf.pages):
            im = page.to_image(resolution=resolution)
            im_data = io.BytesIO()
            im.save(im_data, format='PNG')
            im_bytes_stream = im_data.getvalue()
            im_bytes.append((file_name % (int(i) + 1), bytes(im_bytes_stream)))
    return im_bytes

def create_zip_stream(files):
    zip_buff = io.BytesIO()
    with zipfile.ZipFile(zip_buff, 'w') as zip_file:
        for file_name, file_content in files:
            zip_file.writestr(file_name, file_content)
    zip_buff.seek(0)
    return zip_buff

def send_img(file_obj, file_name, resolution):
    file_name = file_name[:file_name.index('.')]
    im_bytes = get_im_bytes(file_obj, file_name, resolution)
    zip_buff = create_zip_stream(im_bytes)
    return send_file(zip_buff, as_attachment=True, mimetype='application/zip', download_name=file_name + '.zip') 

def send_imgs(file_objs, resolution):
    imgs = []
    for file_name, file_obj in file_objs:
        file_name = file_name[:file_name.index('.')]
        im_bytes = get_im_bytes(file_obj, file_name, resolution)
        zip_buff = create_zip_stream(im_bytes)
        zip_stream = zip_buff.getvalue()
        imgs.append((file_name + '.zip', bytes(zip_stream)))
    buff = create_zip_stream(imgs)
    return send_file(buff, as_attachment=True, mimetype='application/zip', download_name='files.zip') 

@app.route("/")
def index():
    try:
        with open(home_path + 'README.md', 'r', encoding='utf-8') as f:
            content = f.read()
            html = md.markdown(content)
            return Response(html, mimetype='text/html')
    except:
        return "README.md is missing", 400

@app.route("/example")
def example():
    try:
        with open(home_path + 'example.html', 'r', encoding='utf-8') as f:
            html = f.read()
            return Response(html, mimetype='text/html')
    except:
        return "Page is not found", 400

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"info" : "No file part"})

    if 'resolution' not in request.form:
        return jsonify({"info" : "Resolution must be filled in form"})
 
    file = request.files['file']
    if file.filename == '':
        return jsonify({"info" : "No selected file"})
 
    if file:
        filename = secure_filename(file.filename) 
        bytes_io = io.BytesIO(file.stream.read())
        return send_img(bytes_io, filename, int(request.form["resolution"]))

@app.route('/uploads', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        return jsonify({"info" : "No file part"})
 
    if 'resolution' not in request.form:
        return jsonify({"info" : "Resolution must be filled in form"})

    files = request.files.getlist('files')
    file_objs = []
    for file in files:
        if file.filename == '':
            return jsonify({"info" : "No selected file"})
 
        if file:
            filename = secure_filename(file.filename)
            bytes_io = io.BytesIO(file.stream.read())
            file_objs.append((filename, bytes_io))
            
    return send_imgs(file_objs, int(request.form["resolution"]))

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=80)
