from flask import jsonify
from flask_cors import CORS

from flask import Blueprint
from backend.data_process import init_data, download_csv

bp = Blueprint("views", __name__)
cors = CORS(bp, resources={r"/getMsg": {"origins": "*"}})


@bp.route('/', methods=('Get', 'Post'))
def index():
    init_data()
    return "Hello Project Lab!"


@bp.route('/getMsg', methods=['GET','POST'])
def home():
    response = {
        'msg':'Hello, This is a simple demo!'
    }
    return jsonify(response)
