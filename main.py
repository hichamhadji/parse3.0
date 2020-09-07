import os
import urllib.request
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from trade_finance.tf import *
from margin_call.mc import *

app = Flask(__name__)
app.config['UPLOAD_FOLDER_MC'] = './margin_call/UPLOAD_FOLDER'
app.config['UPLOAD_FOLDER_TF'] = './trade_finance/UPLOAD_FOLDER'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS_MARGIN = set(['msg'])
ALLOWED_EXTENSIONS_TF = set(['pdf'])

def allowed_file(filename,margin=True):
	if margin:
		return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_MARGIN
	else:
		return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_TF

@app.route('/intelligent-doc-automation/margin-call/api/v1/document', methods=['POST'])
def margin_call():
	if not os.path.exists(app.config['UPLOAD_FOLDER_MC']):
		os.mkdir(app.config['UPLOAD_FOLDER_MC'])
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file_path = os.path.join(app.config['UPLOAD_FOLDER_MC'], os.path.join(filename.rsplit('.',1)[0]))
		if not os.path.exists(file_path):
			os.mkdir(file_path)
		full_file_path = os.path.join(file_path,filename)
		file.save(full_file_path)
		return margin_output(full_file_path)
	else:
		resp = jsonify({'message' : 'Allowed file type is pdf'})
		resp.status_code = 400
		return resp

@app.route('/intelligent-doc-automation/trade-finance/api/v1/document', methods=['POST'])
def trade_finance():
		# check if the post request has the file part
		if 'file' not in request.files:
				resp = jsonify({'message' : 'No file part in the request'})
				resp.status_code = 400
				return resp
		file = request.files['file']
		if file.filename == '':
				resp = jsonify({'message' : 'No file selected for uploading'})
				resp.status_code = 400
				return resp
		if file and allowed_file(file.filename,margin=False):
				filename = secure_filename(file.filename)
				if not os.path.exists(app.config['UPLOAD_FOLDER_TF']):
					os.mkdir(app.config['UPLOAD_FOLDER_TF'])
				file_path = os.path.join(app.config['UPLOAD_FOLDER_TF'],filename)
				file.save(file_path)
				return trade_output(filename)
		else:
				resp = jsonify({'message' : 'Allowed file type is pdf'})
				resp.status_code = 400
				return resp

@app.route('/',methods=['GET','POST'])
def test():
	return ('working')

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int("4900"), debug=True)
