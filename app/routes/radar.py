from config import RADAR_FOLDER, ALLOWED_IMAGE_EXTENSIONS
from flask import render_template, request, redirect, url_for, Blueprint
from werkzeug.utils import secure_filename
import os
from PIL import Image
import re

radar_bp = Blueprint('radar', __name__, url_prefix='/upload/radar')

#Check for image file format
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
            if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
                filename = secure_filename(file.filename)
                name = sanitize_filename(filename)
                file.save(os.path.join(RADAR_FOLDER, filename))
                return redirect(url_for('radar.show_result', parquet_file=filename, success_message='Radar image uploaded successfully!'))
            else:
                return redirect(url_for('radar.show_result', error='Invalid file format. Please upload a JPEG or JPG image.'))
        else:
            if file and allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
                filename = secure_filename(file.filename)
                file.save(os.path.join(RADAR_FOLDER, filename))
                return redirect(url_for('radar.show_result', radar_file=filename, success_message='Radar image uploaded successfully!'))
            else:
                return redirect(url_for('radar.show_result', error='Invalid file format. Please upload a JPEG or JPG image.'))
    return render_template('upload_radar.html')

#Return Result HTML page for GET
@radar_bp.route('/result', methods=['GET'])
def show_result():
    radar_file = request.args.get('radar_file')
    error_message = request.args.get('error_message')
    success_message = request.args.get('success_message')
    
    if radar_file:
        radar_path = os.path.join(RADAR_FOLDER, radar_file)
        radar_info = get_radar_info(radar_path)
        print(radar_info)
        if radar_info:
            return render_template('radar_result.html', radar_info=radar_info, success_message=success_message, error_message=error_message)
        else:
            error_message = 'Error processing radar image.'
    
    return render_template('radar_result.html', error_message=error_message)

def get_image_url(filename): 
    return f"/static/radars/{filename}"

def get_radar_info(radar_path):
    try:
        with Image.open(radar_path) as image:
            filename = os.path.basename(radar_path)
            file_size = os.path.getsize(radar_path)
            dimensions = f"{image.width}x{image.height}"
            
            return {
                'weburl': get_image_url(filename),
                'filename': filename,
                'file_size': file_size,
                'dimensions': dimensions
            }
    except Exception as e:
        print(f"Error processing radar image: {str(e)}")
        return None
