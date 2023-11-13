from config import PARQUET_FOLDER, RADAR_FOLDER
from flask import render_template, request, Blueprint
import os
from ProcessGameState import ProcessGameState

game_state_bp = Blueprint('game_state', __name__)

@game_state_bp.route('/game-state-processing', methods=['GET', 'POST'])
def game_state_processing():
    parquet_files = os.listdir(os.path.join(PARQUET_FOLDER))
    radar_files = os.listdir(os.path.join(RADAR_FOLDER))

    #If HTML page submits POST --> process the selected parquet file and radar image using the ProcessGameState class
    if request.method == 'POST':
        selected_parquet = request.form['parquet']
        selected_radar = request.form['radar']
        boundaries = request.form.getlist('boundary')

        # TODO: Process the selected parquet file and radar image using the ProcessGameState class
        

        return render_template('game_state_processing.html', parquet_files=parquet_files, radar_files=radar_files,
                               boundaries=boundaries, message='Processing complete!')

    #GET --> return html page
    return render_template('game_state_processing.html', parquet_files=parquet_files, radar_files=radar_files)
