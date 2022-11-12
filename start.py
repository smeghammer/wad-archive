import pymongo
import requests
from config.settings import settings
from libs.database import WadArchiveDatabase



import json
from flask import Flask, jsonify, send_file, render_template, request

from libs.middleware import Middleware

app = Flask(__name__)
mware = Middleware(settings)
    
@app.route('/')
@app.route('/index')
def index():
    '''
    endpoint for returning rendered template homepage
    '''
    return render_template('index.html', title='WAD Archive')

@app.route('/app')
def approot():
    return "Application API root"

@app.route('/app/count')
def filecount():
    '''
    endpoint for returning unfiltered filecount. superceded by return data from pagedfiles
    '''
    return str(mware.filecount())

# https://www.folkstalk.com/2022/10/flask-arguments-in-url-with-code-examples.html
@app.route('/app/files/<int:page_size>/<int:page_num>')
def pagedfiles(page_size,page_num):
    '''
    endpoint for returning a paged list of filenames
    '''
    filter = request.args.get('filter', default = None, type = str)
    result = mware.files(settings['records_per_page'],page_num, filter)
    return result

# https://stackoverflow.com/questions/57564873/how-to-download-in-memory-zip-file-object-using-flask-send-file
@app.route('/app/file/<guid>')
def file(guid):
    '''
    endpoint for returnig binary file data. This is the core of this application:
    '''
    return_file, file_name = mware.file(guid)
    try:
        return send_file(return_file, 'application/x-doom', False, file_name)
    except Exception as ex:
        print('file not found')

@app.route('/app/file/readme/<guid>')
def readme(guid):
    '''
    endpoint for returning readme. will be incorporated into app/file/details/<guid> complex return structure
    '''
    return mware.readme(guid)

@app.route('/app/file/details/<guid>')
def details(guid):
    return mware.details(guid)

app.run()

