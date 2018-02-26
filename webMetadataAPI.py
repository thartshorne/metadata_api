#!/usr/bin/env python
# Application logic for FFCWS metadata API.
# Last modified: 25 February 2018

import os
import datetime
import logging
import uuid
import json
from logging.handlers import RotatingFileHandler
from flask import Flask, request, render_template, url_for, send_file, make_response
from flask_sqlalchemy import SQLAlchemy

# Instantiate Flask app
application = Flask(__name__)

# Configure application
application.config.from_envvar('APP_CONFIG', silent=True)
db = SQLAlchemy(application)


# Datetime helper
epoch_base = datetime.datetime.utcfromtimestamp(0)
def epochalypse_now():
    return int((datetime.datetime.now() - epoch_base).total_seconds())


## Core API views ##
## TODO ##

@app.route("/select")
def selectMetadata():
    pass
    # global metadata
    #
    # varName = request.args.get('varName').decode('utf-8')
    # if varName is None:
    #     return('Error: please enter a varName')
    # fieldName = request.args.get('fieldName', default=None)
    # return app.response_class(metadata.select(varName, fieldName), content_type='application/json')

@app.route("/filter")
def filterMetadata():
    pass
    # global metadata
    #
    # filters = {}
    # for query in request.args:
    #     filters[query] = request.args.get(query).decode('utf-8')
    # if filters == {}:
    #     return app.response_class(metadata.filter(), content_type='application/json')
    # else:
    #     return app.response_class(metadata.filter(filters), content_type='application/json')

@app.route("/search")
def searchMetadata():
    pass
    # global metadata
    #
    # query = request.args.get('query').decode('utf-8')
    # if query is None:
    #     return ('Error: please enter a query')
    # return app.response_class(metadata.search(query), content_type='application/json')


## Static pages ##

# Full metadata file download
@application.route('/get_metadata')
def metadata():
    return send_file(application.config["METADATA_FILE"], as_attachment=True),

# Feedback page
@application.route("/feedback")
def feedback():
    return render_template('feedback.html')

# Landing page with API documentation
# Also, set a unique ID for this user
@application.route("/")
def landing():
    resp = make_response(render_template('index.html'))

    # Set cookie data if not found
    if not request.cookies.get("user_id"):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
        g_uuid = str(uuid.uuid4())
        resp.set_cookie("user_id", g_uuid, expires=expire_date)

    # Render index page
    return resp


# Execute app directly when invoked
if __name__ == "__main__":
    # Configure logging (save 10mb of logs in chunks of 1mb)
    handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024, backupCount=10)
    handler.setLevel(logging.INFO)
    application.logger.addHandler(handler)
    application.logger.setLevel(logging.INFO)
    application.logger.info("[{}] App launched.".format(epochalypse_now()))

    # Launch application
    application.run(host="0.0.0.0")
