from config import PARQUET_FOLDER, ALLOWED_PARQUET_EXTENSIONS
from flask import render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import secure_filename
import os
import pandas as pd
import re

parquet_bp = Blueprint('parquet', __name__, url_prefix='/upload/parquet')

#Check for Parquet file format
def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

#Sanitize filename
def sanitize_filename(filename):
    return re.sub(r'[^A-Za-z0-9-_]', '', filename)

#Upload for POST
#redirect(url_for) -> GET request for show_result
def action_upload():
    if request.method == 'POST':
        file = request.files['file']
        name = request.form['name'].strip()
        if not name:
            if file and allowed_file(file.filename, ALLOWED_PARQUET_EXTENSIONS):
                filename = secure_filename(file.filename)
                name = sanitize_filename(filename)
                file.save(os.path.join(PARQUET_FOLDER, filename))
                return redirect(url_for('parquet.show_result', parquet_file=filename, success_message='Parquet file uploaded successfully!'))
            else:
                return redirect(url_for('parquet.show_result', error_message='Invalid file format. Please upload a parquet file.'))
        else:
            nameWithExtension = f'{name}.parquet'
            if file and allowed_file(nameWithExtension, ALLOWED_PARQUET_EXTENSIONS):
                filename = secure_filename(nameWithExtension)
                file.save(os.path.join(PARQUET_FOLDER, filename))
                return redirect(url_for('parquet.show_result', parquet_file=filename, success_message='Parquet file uploaded successfully!'))
            else:
                return redirect(url_for('parquet.show_result', error_message='Invalid file format. Please upload a parquet file.'))
    return render_template('upload_parquet.html')

#Return Result HTML page for GET
@parquet_bp.route('/result', methods=['GET'])
def show_result():
    parquet_file = request.args.get('parquet_file')
    error_message = request.args.get('error_message')
    success_message = request.args.get('success_message')

    if parquet_file:
        try:
            parquet_path = os.path.join(PARQUET_FOLDER, parquet_file)
            df = pd.read_parquet(parquet_path)
            head_columns = df.columns.tolist()
            row_count = len(df)
            return render_template('parquet_result.html', head_columns=head_columns, row_count=row_count,
                                   success_message=success_message, error_message=error_message)
        except Exception as e:
            error_message = 'Error processing parquet file.'
            return render_template('parquet_result.html', error_message=error_message)
    else:
        return redirect(url_for('upload.index'))
