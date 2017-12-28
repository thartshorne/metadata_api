from flask import Flask
from flask import request
import json
import sys
import localMetadataAPI
app = Flask(__name__)

metadata = localMetadataAPI.Metadata()

@app.route("/")
def landing():
	select = "Select Metadata (fieldName optional):<br/> /select?varName=x&fieldName=y<br/><br/>"
	filte = "Filter Metadata (provide any fields as filters):<br/> /filter?field1=x&field2=y&field3=z<br/><br/>"
	search = "SearchMetadata (provide both a query string and a search field):<br/> /search?query=x&fieldName=y<br/><br/>"
	return select + filte + search

@app.route("/select")
def selectMetadata():
	global metadata

	varName = request.args.get('varName')
	if varName is None:
		return('Error: please enter a varName')
	fieldName = request.args.get('fieldName', default=None)
	return app.response_class(metadata.selectMetadata(varName, fieldName), content_type='application/json')
