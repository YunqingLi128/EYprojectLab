# from flask import Flask
# from flask import jsonify
# from flask_cors import CORS
#
# app = Flask(__name__)
# # cors = CORS(app, resources={r"/getMsg": {"origins": "*"}})
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
# @app.route('/getMsg', methods=['GET','POST'])
# def home():
#     response = {
#         'msg':'Hello, This is a simple demo!'
#     }
#     return jsonify(response)
#
# @app.route('/getDataByCompanyID/<int:id>')
# def getDataByCompanyID(id):
#     response = {
#         # TODO: replace with the real data.
#         'name': "Sample Company name",
#         'companyID' : id,
#         'length': 5,
#         'xdata': [1,2,3,4,5],
#         'ydata': [11,22,33,44,55]
#     }
#     return jsonify(response)
#
# if __name__ == '__main__':
#     app.run()