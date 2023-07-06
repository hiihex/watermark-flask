from flask import Blueprint, render_template, flash, redirect, url_for, request, send_file
from .utils import allowed_file, create_zip_file

bp = Blueprint('', __name__, url_prefix='/')


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/upload/', methods=['GET', 'POST'])
def upload():
    if request.method != 'POST':
        return redirect(url_for('index'))

    files = request.files.getlist("files")
    watermark = request.files.getlist("watermark")

    if len(request.files) <= 0 or (files[0].filename == '' and files[0].mimetype == 'application/octet-stream'):
        flash('You did not upload any files', 'danger')
        return redirect(url_for('index'))

    if watermark[0].filename == '' and watermark[0].mimetype == 'application/octet-stream':
        flash('You did not upload a watermark', 'danger')
        return redirect(url_for('index'))

    for file in files:
        if not allowed_file(file.filename):
            flash('You can only upload image files. Please try again', 'danger')
            return redirect(url_for('index'))

    zip_bytes = create_zip_file(files, watermark)

    return send_file(zip_bytes,
                     download_name='images.zip',
                     mimetype='zip',
                     as_attachment=True)
