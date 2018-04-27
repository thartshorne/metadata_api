from flask import Flask

from ffmeta import settings


def create_app(debug=False):

    app = Flask('ffmeta')
    app.config.from_pyfile('settings.py')

    if debug:
        from werkzeug.debug import DebuggedApplication
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

    import ffmeta.blueprints.api

    app.register_blueprint(ffmeta.blueprints.api.bp, url_prefix='/')
    app.teardown_appcontext_funcs = (shutdown_session, )
    return app


def shutdown_session(exception=None):
    from ffmeta.models.db import session
    session.remove()
