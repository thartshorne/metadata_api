import datetime
import os.path
import uuid

from flask import Blueprint, request, Response, jsonify, make_response, send_file, send_from_directory, render_template, current_app

from ffmeta.models.db import session
from ffmeta.models import Response, Variable, Umbrella, Topic
from ffmeta.utils import api_error, epochalypse_now, dedupe_varlist, search_db

bp = Blueprint('api', __name__)


@bp.route("/select")
def selectMetadata():
    # Get request data
    varname = request.args.get("varName")
    fieldname = request.args.get('fieldName', default=None)

    # Error out if varname not provided
    if not varname:
        return api_error(400, "Variable name not provided.")

    # Get variable data (abort if not valid)
    var = session.query(Variable).filter(Variable.name == varname).first()
    if not var:
        return api_error(400, "Invalid variable name.")
    var_data = var.serialize

    # Append topics
    topics = session.query(Topic).filter(Topic.name == varname).group_by(Topic.topic).all()
    umbrellas = session.query(Umbrella).filter(Umbrella.topic.in_([str(t.topic) for t in topics])).all()
    var_data["topics"] = [{"umbrella": str(u.umbrella), "topic": str(u.topic)} for u in umbrellas]

    # Append responses
    responses = session.query(Response).filter(Response.name == varname).group_by(Response.label).all()
    var_data["responses"] = {value: label for (value, label) in [(r.value, r.label) for r in responses]}

    # Error out if field name not valid
    if fieldname and fieldname not in var_data.keys():
        return api_error(400, "Invalid field name.")

    # Log query
    current_app.logger.info("{}\t{}\tselectMetadata\tname: {}\tfield: {}".format(epochalypse_now(), request.cookies.get("user_id"), varname, str(fieldname)))

    # Return only a single field if specified
    if not fieldname:
        rv = jsonify(var_data)
    else:
        result = {fieldname: var_data[fieldname]}
        rv = jsonify(result)

    resp = make_response(rv)

    # Set cookie data if not found
    if not request.cookies.get("user_id"):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
        g_uuid = str(uuid.uuid4())
        resp.set_cookie("user_id", g_uuid, expires=expire_date)

    return resp


@bp.route("/filter")
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
    current_app.logger.info("{}\t{}\tfilterMetadata\tfilters: {}".format(epochalypse_now(), request.cookies.get("user_id"), list(request.args.items())))

    # Return list of matches
    if not found:
        rv = jsonify({"matches": []})
    else:
        varlist = dedupe_varlist(found)
        rv = jsonify({"matches": varlist})

    resp = make_response(rv)

    # Set cookie data if not found
    if not request.cookies.get("user_id"):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
        g_uuid = str(uuid.uuid4())
        resp.set_cookie("user_id", g_uuid, expires=expire_date)

    return resp


@bp.route("/search")
def searchMetadata():
    # Get request data
    querystr = request.args.get("query")
    fieldname = request.args.get('fieldName', default=None)

    # Error out if query or field not provided
    if not querystr:
        return api_error(400, "Query string not specified.")
    if not fieldname:
        return api_error(400, "Field name to search not specified.")

    # Search by table
    matches = search_db(fieldname, querystr)

    # Log query
    current_app.logger.info("{}\t{}\tsearchMetadata\tquery: {}\tfieldname: {}".format(epochalypse_now(), request.cookies.get("user_id"), querystr, fieldname))

    # Yield a list of variable names
    if not matches:
        rv = jsonify({"matches": []})
    else:
        rv = jsonify({"matches": matches})

    resp = make_response(rv)

    # Set cookie data if not found
    if not request.cookies.get("user_id"):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
        g_uuid = str(uuid.uuid4())
        resp.set_cookie("user_id", g_uuid, expires=expire_date)

    return resp

# Static pages #


# Favicon
@bp.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Full metadata file download
@bp.route('/get_metadata')
def metadata():
    # Log query
    current_app.logger.info("{}\t{}\tfull-file-download".format(epochalypse_now(), request.cookies.get("user_id")))
    return send_file(current_app.config["METADATA_FILE"], as_attachment=True),


# Feedback page
@bp.route("/feedback")
def feedback():
    return render_template('feedback.html')


# Landing page with API documentation
# Also, set a unique ID for this user
@bp.route("/")
def landing():
    resp = make_response(render_template('index.html'))

    # Set cookie data if not found
    if not request.cookies.get("user_id"):
        expire_date = datetime.datetime.now() + datetime.timedelta(days=90)
        g_uuid = str(uuid.uuid4())
        resp.set_cookie("user_id", g_uuid, expires=expire_date)

    # Log query
    current_app.logger.info("{}\t{}\thome".format(epochalypse_now(), request.cookies.get("user_id")))

    # Render index page
    return resp
