from flask import jsonify
from flask import request
from flask_cors import CORS
from flask import Blueprint

from backend.data_process import data_preprocessing
from backend.backend_analysis_plotting import VaR_sVarR_comparison
from backend.backend_analysis_plotting import advanced_market_risk_weighted_assets
from backend.backend_analysis_plotting import VaR_based_measure_overtime
from backend.backend_analysis_plotting import sVaR_VaR_ratio_overtime
from backend.backend_analysis_plotting import trading_asset_comparison
from backend.backend_analysis_plotting import num_var_breach_overtime
from backend.backend_analysis_plotting import var_by_assetclass_diversification
from backend.backend_analysis_plotting import standardized_risk_weighted_assets
from backend.backend_analysis_plotting import diverse_of_var_overtime

bp = Blueprint("views", __name__)
# cors = CORS(bp, resources={r"/getMsg": {"origins": "*"}})
CORS(bp, supports_credentials=True)


@bp.route('/', methods=('Get', 'Post'))
def index():
    data_info = data_preprocessing()
    return jsonify(data_info)


@bp.route('/getMsg', methods=['GET','POST'])
def home():
    response = {
        'msg':'Hello, This is a simple demo!'
    }
    return jsonify(response)

@bp.route('/getDataByCompanyID/<int:id>')
def getDataByCompanyID(id):
    # response = {
    #     # TODO: replace with the real data.
    #     'name': "Sample Company name",
    #     'companyID' : id,
    #     'length': 5,
    #     'xdata': [1,2,3,4,5],
    #     'ydata': [11,22,33,44,55]
    # }
    data = test_VaR_sVarR_query('2017Q4')
    response = {
        'item': ['Company', 'VaR', 'SVaR'],
        'data': data
    }
    return jsonify(response)

@bp.route('/getTradingAssetComparison', methods=['GET'])
def getTradingAssetComparison():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    res = trading_asset_comparison(start_quarter, end_quarter)
    return jsonify(res)

@bp.route('/getVaRsVarRComparisonQuery', methods=['GET'])
def getVaRsVarRComparisonQuery():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    res = VaR_sVarR_comparison(start_quarter, end_quarter)
    return jsonify(res)

@bp.route('/getAdvancedMarketRiskWeightedAssets', methods=['GET'])
def getAdvancedMarketRiskWeightedAssets():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    res = advanced_market_risk_weighted_assets(start_quarter, end_quarter)
    return jsonify(res)

@bp.route('/getChangeInVaRBasedMeasureOvertime', methods=['GET'])
def getChangeInVaRBasedMeasureOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    res = VaR_based_measure_overtime(start_quarter, end_quarter)
    return jsonify(res)

@bp.route('/getVaRsVaRRatioOvertime', methods=['GET'])
def getVaRsVaRRatioOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    res = sVaR_VaR_ratio_overtime(start_quarter, end_quarter)
    return jsonify(res)

@bp.route('/getDiversificationVaROvertime', methods=['GET'])
def diversification_of_var_overtime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    res = sVaR_VaR_ratio_overtime(start_quarter, end_quarter)
    return jsonify(res)

@bp.route('/getVaRBreachOvertime', methods=['GET'])
def getVaRBreachOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    res = num_var_breach_overtime(start_quarter, end_quarter)
    return jsonify(res)

@bp.route('/getVaRByAssetClassDiversification', methods=['GET'])
def getVaRByAssetClassDiversification():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    res = var_by_assetclass_diversification(start_quarter, end_quarter)
    return jsonify(res)

@bp.route('/getStandardizedRiskWeightedAssets', methods=['GET'])
def getStandardizedRiskWeightedAssets():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    res = standardized_risk_weighted_assets(start_quarter, end_quarter)
    return jsonify(res)

@bp.route('/getDiversificationVarOvertime', methods=['GET'])
def getDiversificationVarOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    res = diverse_of_var_overtime(start_quarter, end_quarter)
    return jsonify(res)



