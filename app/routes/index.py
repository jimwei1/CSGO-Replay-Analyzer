from flask import render_template, Blueprint
import pandas as pd

index_bp = Blueprint('index', __name__)

@index_bp.route('/', methods=['GET'])
def index():

  #Return home HTML page
  return render_template('home.html')
