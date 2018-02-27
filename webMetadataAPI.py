#!/usr/bin/env python
# Application logic for FFCWS metadata API.
# Last modified: 25 February 2018

import os
import datetime
import logging
import uuid
import json
from logging.handlers import RotatingFileHandler
from flask import Flask, request, render_template, url_for, send_file, send_from_directory, make_response, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

# Instantiate Flask app
application = Flask(__name__)

# Configure application
application.config.from_envvar('APP_CONFIG', silent=True)
db = SQLAlchemy(application)


# Define data models
class Variable(db.Model):
    __tablename__ = "variable"

    # Define table fields
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    label = db.Column(db.Text)
    old_name = db.Column(db.Text)
    data_type = db.Column(db.Text)
    warning = db.Column(db.Integer)
    group_id = db.Column(db.Text)
    group_subid = db.Column(db.Text)
    data_source = db.Column(db.Text)
    respondent = db.Column(db.Text)
    wave = db.Column(db.Text)
    scope = db.Column(db.Text)
    section = db.Column(db.Text)
    leaf = db.Column(db.Text)

    def __init__(self, name, label, old_name, data_type, warning, group_id, group_subid, data_source, respondent, wave, scope, section, leaf):
        self.name = name
        self.label = label
        self.old_name = old_name
        self.data_type = data_type
        self.warning = warning
        self.group_id = group_id
        self.group_subid = group_subid
        self.data_source = data_source
        self.respondent = respondent
        self.wave = wave
        self.scope = scope
        self.section = section
        self.leaf = leaf

    def __repr__(self):
        return "<Variable %r>" % self.name

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "label": self.label,
            "old_name": self.old_name,
            "data_type": self.data_type,
            "warning": self.warning,
            "group_id": self.group_id,
            "group_subid": self.group_subid,
            "data_source": self.data_source,
            "respondent": self.respondent,
            "wave": self.wave,
            "scope": self.scope,
            "section": self.section,
            "leaf": self.leaf
        }

class Topic(db.Model):
    __tablename__ = "topic"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    topic = db.Column(db.Text)

    def __init__(self, name, topic):
        self.name = name
        self.topic = topic

    def __repr__(self):
        return "<Topic %r>" % self.topic

class Umbrella(db.Model):
    __tablename__ = "umbrella"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.Text)
    umbrella = db.Column(db.Text)

    def __init__(self, topic, umbrella):
        self.topic = topic
        self.umbrella = umbrella

    def __repr__(self):
        return "<Umbrella %r>" % self.umbrela

class Response(db.Model):
    __tablename__ = "response"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    label = db.Column(db.Text)
    value = db.Column(db.Integer)

    def __init__(self, name, label, value):
        self.name = name
        self.label = label
        self.value = value

    def __repr__(self):
        return "<Response %r>" % self.label

class Group(db.Model):
    __tablename__ = "group"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Text)
    count = db.Column(db.Integer)

    def __init__(self, group_id, count):
        self.group_id = group_id
        self.count = count

    def __repr__(self):
        return "<Group %r>" % self.group_id


## Helper functions ##

# Datetime helper
epoch_base = datetime.datetime.utcfromtimestamp(0)
def epochalypse_now():
    return int((datetime.datetime.now() - epoch_base).total_seconds())

# Throw informative API errors as JSON
def api_error(code, description):
    error = jsonify({"error code": code, "error_description": description})
    return error

# Deduplicate a list
def dedupe_varlist(varlist):
    seen = set()
    seen_add = seen.add
    return [x for x in varlist if not (x in seen or seen_add(x))]

# Search database for variable names where field matches value at least partially
# Secretly, both filter and search use this functionality!
def search_db(field, value):
    matches = None
    if field == "umbrella":
        # Get all variables in all topics with matching umbrellas
        topics_found = Umbrella.query.filter((Umbrella.umbrella.like('%%{}%%'.format(value))) | (Umbrella.topic.like('%%{}%%'.format(value)))).all()
        tlist = [t.topic for t in topics_found]
        matches = Topic.query.filter(Topic.topic.in_(tlist)).group_by(Topic.topic, Topic.name).all()
    elif field == "topic":
        matches = Topic.query.filter(Topic.topic.like('%%{}%%'.format(value))).all()
    elif field == "responses":
        matches = Response.query.filter(Response.label.like('%%{}%%'.format(value))).all()
    else:
        # Throw out anything else that's not in Variable
        if field not in Variable.__table__.columns:
            api_error(400, "Invalid field name.")

        # All other variable metadata is stored with the variables
        fieldobj = eval("Variable.{}".format(field))
        matches = Variable.query.filter(fieldobj.like('%%{}%%'.format(value))).all()

    # Return variable names found, deduplicated
    distinct = dedupe_varlist([m.name for m in matches])
    return distinct


## Core API views ##

@application.route("/select")
def selectMetadata():
    # Get request data
    varname = request.args.get("varName").decode('utf-8')
    fieldname = request.args.get('fieldName', default=None)

    # Error out if varname not provided
    if not varname:
        return api_error(400, "Variable name not provided.")

    # Get variable data (abort if not valid)
    var = Variable.query.filter(Variable.name == varname).first()
    if not var:
        return api_error(400, "Invalid variable name.")
    var_data = var.serialize

    # Append topics
    topics = Topic.query.filter(Topic.name == varname).group_by(Topic.topic).all()
    umbrellas = Umbrella.query.filter(Umbrella.topic.in_([str(t.topic) for t in topics])).all()
    var_data["topics"] = [{"umbrella": str(u.umbrella), "topic": str(u.topic)} for u in umbrellas]

    # Append responses
    responses = Response.query.filter(Response.name == varname).group_by(Response.label).all()
    var_data["responses"] = {value: label for (value, label) in [(r.value, r.label) for r in responses]}

    # Error out if field name not valid
    if fieldname and fieldname not in var_data.keys():
        return api_error(400, "Invalid field name.")

    # Log query
    application.logger.info("{}\t{}\tselectMetadata\tname: {}\tfield: {}".format(epochalypse_now(), request.cookies.get("user_id"), varname, str(fieldname)))

    # Return only a single field if specified
    if not fieldname:
        return jsonify(var_data)
    else:
        result = {fieldname: var_data[fieldname]}
        return jsonify(result)

@application.route("/filter")
def filterMetadata():
    # Get request data
    fields = request.args.keys()

    # Error out if no fields provided
    if not fields:
        return api_error(400, "Fields to search not provided.")

    # Construct filter object
    found = []
    for field in fields:
        for value in request.args.getlist(field):
            found.extend(search_db(field, value))

    # Log query
    application.logger.info("{}\t{}\tfilterMetadata\tfilters: {}".format(epochalypse_now(), request.cookies.get("user_id"), request.args.items()))

    # Return list of matches
    if not found:
        return jsonify({"matches": []})
    else:
        varlist = dedupe_varlist(found)
        return jsonify({"matches": varlist})


@application.route("/search")
def searchMetadata():
    # Get request data
    querystr = request.args.get("query").decode('utf-8')
    fieldname = request.args.get('fieldName', default=None)

    # Error out if query or field not provided
    if not querystr:
        return api_error(400, "Query string not specified.")
    if not fieldname:
        return api_error(400, "Field name to search not specified.")

    # Search by table
    matches = search_db(fieldname, querystr)

    # Log query
    application.logger.info("{}\t{}\tsearchMetadata\tquery: {}\tfieldname: {}".format(epochalypse_now(), request.cookies.get("user_id"), querystr, fieldname))

    # Yield a list of variable names
    if not matches:
        return jsonify({"matches": []})
    else:
        return jsonify({"matches": matches})


## Static pages ##

# Favicon
@application.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
    handler = RotatingFileHandler('api.log', maxBytes=1024 * 1024, backupCount=10)
    handler.setLevel(logging.INFO)
    application.logger.addHandler(handler)
    application.logger.setLevel(logging.INFO)
    application.logger.info("[{}] App launched.".format(epochalypse_now()))

    # Launch application
    application.run(host="0.0.0.0")
