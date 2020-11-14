import os
import io
import json
import flask
import requests
from datetime import datetime
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from PIL import Image



UPLOAD_FOLDER = '/TestApp/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
POST_COUNTER = 0


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    

def resize_image(image_path, size):
    orig_image = Image.open(image_path).convert('L')
    resized_image = orig_image.resize(size)
    resized_image.save(image_path)


@app.route('/upload/<image>', methods= ['GET'])
def get_image(image):
    return redirect(url_for('static', filename=image))


@app.route('/upload', methods= ['GET'])
def get_render():
    if 'image' in request.args:
        return render_template('upload.html', filename=request.args['image']) 
    else:
        return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload_file():  

    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)   

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_path = UPLOAD_FOLDER + '/' + file.filename

        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        resize_image(image_path, (512, 512))           
    
    return redirect(url_for('get_render', image=file.filename))


@app.route('/', methods=['GET'])
def redirect_to_another_page():
    return redirect(url_for('upload_file'))


@app.route('/', methods=['POST'])
def get_image_json_data():

    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']

    # If user does not select file, browser also
    # submit an empty part without filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        image_path = UPLOAD_FOLDER + '/' + file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Getting JSON data
        date = datetime.now().isoformat()
        img_size = Image.open(image_path).size        
        image_json_data = json.dumps({
                'name': filename, 
                'recieve_date': date,
                'image_size': img_size
                }, sort_keys=True, indent=4)

        resize_image(image_path, (512, 512)) 
    
    return 'Recieved image successfully:\n' + image_json_data + '\n'


if __name__ == '__main__':
    app.run()
