from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import mimetypes

app = Flask(__name__)
base_folder = os.path.basename('downloads')
app.config['UPLOAD_FOLDER'] = base_folder

def check_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3', 'wav', 'ogg'}

def check_mime_files(filename):
    return mimetypes.guess_type(filename)[0]

@app.route('/')
def render_info():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('render_info.html', files=files, mimetypes=mimetypes)

@app.route('/downloads', methods=['POST'])
def download():
    file = request.files['file']
    if file and check_files(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('render_info'))
    else:
        return "Non_audio file detected"
    
@app.route('/downloads/<filename>')
def print_file(filename):
    if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
        mimetype = check_mime_files(filename)
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, mimetype=mimetype)
    else:
        return "File not found", 404

@app.route('/downloads')
def list_of_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('downloads.html', files=files)

if __name__ == '__main__':
    app.run(port=8888, debug=True)