import os
import re

UPLOAD_FOLDER = 'app/static'
PARQUET_FOLDER = os.path.join(UPLOAD_FOLDER, 'parquets')
RADAR_FOLDER = os.path.join(UPLOAD_FOLDER, 'radars')
ALLOWED_EXTENSIONS = {'parquet', 'jpeg', 'jpg'}
ALLOWED_PARQUET_EXTENSIONS = {'parquet'}
ALLOWED_IMAGE_EXTENSIONS = {'jpeg', 'jpg'}
ALLOWED_FILENAME_REGEX = re.compile(r'^[A-Za-z0-9-_]+$')
