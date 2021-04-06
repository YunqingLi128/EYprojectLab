import logging
import urllib3
from flask import jsonify, request, Blueprint, session, current_app, redirect, url_for
from flask_cors import CORS
from backend.data_process import load_data_config_file, init_data, add_data
from backend.backend_analysis_plotting import *

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

bp = Blueprint("views", __name__)
# cors = CORS(bp, resources={r"/getMsg": {"origins": "*"}})
CORS(bp, supports_credentials=True)


@bp.route('/home', methods=('GET', 'POST'))
def index():
    """
    Currently if 'data_status' is in data config file, no to update, which needs to be improved
    So we need to add the logic to call init_data() to update the current data
    """
    # TODO: Add conditions to check when to update and call init_data()
    config_info = load_data_config_file()
    institution_info = config_info["institutions"]
    need_update = False
    for rssd_id in institution_info:
        if 'data_status' not in institution_info[rssd_id]:
            need_update = True
    path = os.path.join(get_cur_path(), 'data/raw_data')
    if not os.path.exists(path):
        need_update = True
    data_info = init_data() if need_update else config_info
    comp_dict = {rssd_id: info['Nick'] for rssd_id, info in data_info['institutions'].items()}
    session['data_loaded'] = True
    session["comp_dict"] = comp_dict
    session.permanent = True
    response = jsonify(data_info)
    return response


@bp.route('/getMsg', methods=['GET', 'POST'])
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


def response_processing(result):
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', current_app.config['FRONT_END_HOST'])
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


@bp.route('/getVaRsVarRComparison', methods=['GET'])
def getVaRsVarRComparison():
    quarter = request.args['quarter']
    logging.info("getVaRsVarRComparison comp_dict: %s", session["comp_dict"])
    result = get_VaR_sVaR_item_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getTradingAssetComparison', methods=['GET'])
def getTradingAssetComparison():
    quarter = request.args['quarter']
    result = get_trading_asset_item_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getTradingAssetToRiskRatio', methods=['GET'])
def getTradingAssetToRiskRatio():
    quarter = request.args['quarter']
    result = get_asset_to_var_ratio_item_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getTradingRevenueToVarRatio', methods=['GET'])
def getTradingRevenueToVarRatio():
    quarter = request.args['quarter']
    result = get_revenue_to_var_ratio_item_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getStandardizedRiskWeightedAssets', methods=['GET'])
def getStandardizedRiskWeightedAssets():
    quarter = request.args['quarter']
    result = get_standardized_risk_weighted_assets_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getVaRByAssetClassDiversification', methods=['GET'])
def getVaRByAssetClassDiversification():
    quarter = request.args['quarter']
    result = get_asset_class_var_item_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getTradingAssetsAndChangeByQuarter', methods=['GET'])
def getTradingAssetsAndChangeByQuarter():
    quarter = request.args['quarter']
    result = get_trading_assets_and_change_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getTradingLiabilitiesAndChangeByQuarter', methods=['GET'])
def getTradingLiabilitiesAndChangeByQuarter():
    quarter = request.args['quarter']
    result = get_trading_liabilities_and_change_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getNetTradingAssetAndPercentChange', methods=['GET'])
def getNetTradingAssetAndPercentChange():
    quarter = request.args['quarter']
    result = get_net_trading_asset_and_percent_change_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getGrossTradingAssetAndPercentChange', methods=['GET'])
def getGrossTradingAssetAndPercentChange():
    quarter = request.args['quarter']
    result = get_gross_trading_asset_and_percent_change_by_quarter(quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getAdvancedMarketRiskWeightedAssets', methods=['GET'])
def getAdvancedMarketRiskWeightedAssets():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_risk_weighted_asset_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getChangeInVaRBasedMeasureOvertime', methods=['GET'])
def getChangeInVaRBasedMeasureOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_var_measure_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getVaRsVaRRatioOvertime', methods=['GET'])
def getVaRsVaRRatioOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_ratio_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getVaRBreachOvertime', methods=['GET'])
def getVaRBreachOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_num_var_breach_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getDiversificationVarOvertime', methods=['GET'])
def getDiversificationVarOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    result = get_var_diversification_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return response_processing(result)


@bp.route('/getStressWindowOvertime', methods=['GET'])
def getStressWindowOvertime():
    args = request.args
    start_quarter = args['start']
    end_quarter = args['end']
    res = get_stress_window_item_overtime(start_quarter, end_quarter, session.get("comp_dict"))
    return jsonify(res)


@bp.route('/addDataByID', methods=['GET', 'POST'])
def addData():
    args = request.args
    rssd_id = args['rssd_id']
    name = args['name']
    nick_name = args['nickName']
    res = add_data(rssd_id, name, nick_name)
    return jsonify(res)
