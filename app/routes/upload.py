from flask import Blueprint
import re
from app.routes.parquet import action_upload as action_upload_parquet
from app.routes.radar import action_upload as action_upload_radar

#Routes for uploading parquet and radar files

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

@upload_bp.route('/parquet', methods=['GET', 'POST'])
def upload_parquet():
    return action_upload_parquet()

@upload_bp.route('/radar', methods=['GET', 'POST'])
def upload_radar():
    return action_upload_radar()

