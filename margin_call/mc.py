from margin_call.email_1 import *
from margin_call.margin_classification import *
from margin_call.pdf_to_text import *
import os
from flask import jsonify


def margin_output(full_file_path):
	file_path = full_file_path.rsplit('/',1)[0]
	email_reading(full_file_path)
	margin_call = margin_classification(file_path)
	ofile = pdf_doc_to_text(full_file_path)
	with open(ofile,'r') as f:
		file_content = f.readlines()
	content = []
	for i in range(len(file_content)):
		if not file_content[i].rstrip('\n')=="":
			content.append(file_content[i].rstrip('\n'))
	return jsonify({"attachment_content":content,"margin_call":margin_call})
