from flask import Blueprint
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from app.utils.pdf_utils import get_pdf_text, get_pdf_images
from app.utils.debug_utils import debug_log

files_blueprint = Blueprint('files_blueprint', __name__)

UPLOAD_URL = 'static'
UPLOAD_FOLDER = 'static'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask("REGEX")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@files_blueprint.route('/files', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        response_array = []
        files = request.files.getlist('files[]')
        for file in files:
            file_response = {}
            print("type(file):", type(file))
            print("file.__dict__:", file.__dict__)

            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # PDF
                fileextn = os.path.splitext(filename)[1]
                if fileextn == ".pdf":
                    # Get Text
                    filetext = get_pdf_text(filepath)
                    file_response.update({'text': filetext})

                    # This should be spun off as a separate thread
                    # Get Images
                    get_pdf_images(filepath, UPLOAD_FOLDER)

            fileurl = url_for(UPLOAD_URL, filename=filename, _external=True)
            file_response.update({'url': fileurl})

            response_array.append(file_response)
            api_response = {'files': response_array}
            debug_log("upload_file: api_response=", api_response, active=False)

        return api_response
