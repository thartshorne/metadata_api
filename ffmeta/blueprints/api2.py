from sqlalchemy import inspect

from flask import Blueprint, request, Response, jsonify, make_response, send_file, send_from_directory, render_template, current_app

from ffmeta.models.db import session
from ffmeta.models import Response, Variable, Umbrella, Topic
from ffmeta.utils import api_error, epochalypse_now, dedupe_varlist, search_db

bp = Blueprint('apiv2', __name__)

variable_attrs = [c_attr.key for c_attr in inspect(Variable).mapper.column_attrs]


@bp.route("/variable/<variable_name>")
def select(variable_name):
    obj = session.query(Variable).filter(Variable.name == variable_name).first()
    if obj:
        d = dict((attr, getattr(obj, attr, '')) for attr in variable_attrs)

        # TODO: The following structure is used to maintain compatibility with old behavior
        # Probably it makes sense to reverse the keys/values
        d['responses'] = dict((r.value, r.label) for r in obj.responses)

        # TODO: The following structure is used to maintain compatibility with old behavior
        # A better structure to this would be to simply return an <umbrella_name>: [<topic_names>] dictionary here
        d['topics'] = [{'umbrella': str(t.umbrella), 'topic': str(t)} for t in obj.topics]

        keys = list(request.args.keys()) or d.keys()
        return jsonify(dict((k, d[k]) for k in keys))
    else:
        return api_error(400, "Invalid variable name.")


@bp.route("/variable")
def search():
    name = request.args.get('name').lower().strip()
    val = request.args.get('val')  # May contain embedded '%' as wildcard(s)

    if name in variable_attrs:
        column = getattr(Variable, name)
        results = [v.name for v in session.query(Variable).filter(column.like(val))]
    elif name == 'response':
        results = [r.name for r in session.query(Response).filter(Response.label.like(val))]
    elif name == 'topic':
        results = [t.name for t in session.query(Topic).filter(Topic.topic.like(val))]
    elif name == 'umbrella':
        topic_names = [u.topic_obj.topic for u in session.query(Umbrella).filter(Umbrella.umbrella.like(val))]
        results = [t.name for t in session.query(Topic).filter(Topic.topic.in_(topic_names))]
    else:
        return api_error(400, "Invalid name for search.")

    return jsonify(list(set(results)))