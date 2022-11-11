import pymongo
import requests
from config.settings import settings
from libs.database import WadArchiveDatabase



import json
from flask import Flask, jsonify, send_file, render_template, request

from libs.middleware import Middleware

app = Flask(__name__, 
            static_folder='static'
            # ,template_folder='templates'
            )
mware = Middleware(settings)
    
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='WAD Archive')

@app.route('/app')
def approot():
    return "Application API root"

@app.route('/app/count')
def filecount():
    return str(mware.filecount())

# https://www.folkstalk.com/2022/10/flask-arguments-in-url-with-code-examples.html
@app.route('/app/files/<int:page_size>/<int:page_num>')
def pagedfiles(page_size,page_num):
    filter = request.args.get('filter', default = None, type = str)
    result = mware.files(settings['records_per_page'],page_num, filter)
    return result
    # return mware.files(page_size,page_num, filter)

# https://stackoverflow.com/questions/57564873/how-to-download-in-memory-zip-file-object-using-flask-send-file
@app.route('/app/file/<guid>')
def file(guid):
    return_file, file_name = mware.file(guid)
    print(return_file)
    return send_file(return_file, 'application/x-doom', False, file_name)

app.run()

