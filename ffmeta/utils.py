import datetime
from flask import jsonify

from ffmeta.models import Umbrella, Response, Variable, Topic
from ffmeta.models.db import session

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
    if field == "umbrella":
        # Get all variables in all topics with matching umbrellas
        topics_found = session.query(Umbrella).filter((Umbrella.umbrella.like('%%{}%%'.format(value))) | (Umbrella.topic.like('%%{}%%'.format(value)))).all()
        tlist = [t.topic for t in topics_found]
        matches = Topic.query.filter(Topic.topic.in_(tlist)).group_by(Topic.topic, Topic.name).all()
    elif field == "topic":
        matches = session.query(Topic).filter(Topic.topic.like('%%{}%%'.format(value))).all()
    elif field == "responses":
        matches = session.query(Response).filter(Response.label.like('%%{}%%'.format(value))).all()
    else:
        # Throw out anything else that's not in Variable
        if field not in Variable.__table__.columns:
            api_error(400, "Invalid field name.")

        # All other variable metadata is stored with the variables
        fieldobj = eval("Variable.{}".format(field))
        matches = session.query(Variable).filter(fieldobj.like('%%{}%%'.format(value))).all()

    # Return variable names found, deduplicated
    distinct = dedupe_varlist([m.name for m in matches])
    return distinct
