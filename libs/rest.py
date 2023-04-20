# import json
# from flask import Flask, jsonify, send_file, render_template
#
# from libs.middleware import Middleware
#
# app = Flask(__name__, 
#             static_folder='static',
#             template_folder='templates')
# mware = Middleware()
#
# @app.route('/')
# @app.route('/index')
# def index():
#     # return jsonify({'root':'test'})
#     return render_template('index.html', title='Welcome')
#
# @app.route('/app')
# def approot():
#     return "Application API root"
#
# @app.route('/app/count')
# def filecount():
#     return mware.filecount()
#
# @app.route('/app/files/<int:page_size>/<int:page_num>')
# def pagedfiles(page_size,page_num):
#     return mware.files(page_size,page_num)
#
# # https://stackoverflow.com/questions/57564873/how-to-download-in-memory-zip-file-object-using-flask-send-file
# @app.route('/app/file/<guid>')
# def file(guid):
#     return_file = mware.file(guid)
#     print(return_file)
#     return send_file(return_file, 'application/x-doom', False, 'TEST FILE.pk3.gz')
#
#
# app.run()