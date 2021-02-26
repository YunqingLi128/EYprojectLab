from flask import jsonify
from flask_cors import CORS

from flask import Blueprint
from backend.data_process import init_data, data_preprocessing, download_csv

bp = Blueprint("views", __name__)
cors = CORS(bp, resources={r"/getMsg": {"origins": "*"}})


@bp.route('/', methods=('Get', 'Post'))
def index():
    init_data(False)
    return "Hello Project Lab!"


@bp.route('/getMsg', methods=['GET','POST'])
def home():
    response = {
        'msg':'Hello, This is a simple demo!'
    }
    return jsonify(response)
    
@bp.route('/getDataByCompanyID/<int:id>')
def getDataByCompanyID(id):
    response = {
        # TODO: replace with the real data.
        'name': "Sample Company name",
        'companyID' : id,
        'length': 5,
        'xdata': [1,2,3,4,5],
        'ydata': [11,22,33,44,55]
    }
    return jsonify(response)
