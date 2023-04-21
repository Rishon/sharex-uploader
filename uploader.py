import os
import random
import string
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/uploader/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
SERVER_NAME = 'i.rishon.systems'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SERVER_NAME'] = SERVER_NAME 

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_filename(filename):
    letters = string.ascii_lowercase
    ext = filename.rsplit('.', 1)[1].lower()
    return ''.join(random.choice(letters) for i in range(6)) + '.' + ext


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'})

    if 'secret_code' not in request.form or request.form['secret_code'] != 'your_secret_code':
        return jsonify({'error': 'Unauthorized access'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'})

    if file and allowed_file(file.filename):
        filename = generate_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        url = f"https://{SERVER_NAME}/{filename}"
        return jsonify({'url': url})

    return jsonify({'error': 'File type not allowed'})

@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], ''), filename)

@app.errorhandler(404)
def page_not_found(e):
        return f'''
            <!DOCTYPE html>
            <html>
                <head>
                    <meta http-equiv="refresh" content="0; url=https://rishon.systems/">
                </head>
                <body>
                    <p>uwu</p>
                </body>
            </html> '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2000, debug=False)
