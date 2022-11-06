import pymongo
import requests
from libs.database import WadArchiveDatabase


import json
from flask import Flask, jsonify, send_file, render_template

from libs.middleware import Middleware

app = Flask(__name__, 
            static_folder='static'
            # ,template_folder='templates'
            )
mware = Middleware()
    
@app.route('/')
@app.route('/index')
def index():
    # return jsonify({'root':'test'})
    return render_template('index.html', title='Welcome!!')

@app.route('/app')
def approot():
    return "Application API root"

@app.route('/app/count')
def filecount():
    return str(mware.filecount())

# @app.route('/app/files')
# def files():
#     return mware.files()

@app.route('/app/files/<int:page_size>/<int:page_num>')
def pagedfiles(page_size,page_num):
    
    _TEST = mware.files(page_size,page_num)
    
    return mware.files(page_size,page_num)

# https://stackoverflow.com/questions/57564873/how-to-download-in-memory-zip-file-object-using-flask-send-file
@app.route('/app/file/<guid>')
def file(guid):
    return_file, file_name = mware.file(guid)
    print(return_file)
    return send_file(return_file, 'application/x-doom', False, file_name)


app.run()

# if __name__ == '__main__':

# db = WadArchiveDatabase()
# print(db)
# filenames = db.getFilenames()
#
# counter = 0
# for fname in filenames:
#     counter+=1
#     if len(fname['filenames']):
#         print(fname['filenames'][0],fname['_id'])
#     else:
#         print('NO FILENAME!')
# print(counter,' files') 

''' start the application '''
# print('start')       
# import libs.rest

