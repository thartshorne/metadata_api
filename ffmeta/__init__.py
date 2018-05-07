from flask import Flask, jsonify

from ffmeta import settings
from ffmeta.utils import AppException


def create_app(debug=False):

    def handle_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    app = Flask('ffmeta')
    app.config.from_pyfile('settings.py')

    if debug:
        from werkzeug.debug import DebuggedApplication
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

    import ffmeta.blueprints.api

    app.register_blueprint(ffmeta.blueprints.api.bp, url_prefix='/')
    app.register_error_handler(AppException, handle_error)
    app.teardown_appcontext_funcs = (shutdown_session, )
    return app


def shutdown_session(exception=None):
    from ffmeta.models.db import session
    session.remove()
