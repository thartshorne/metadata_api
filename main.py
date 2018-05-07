import logging
from logging.handlers import RotatingFileHandler

from ffmeta import create_app
from ffmeta.settings import DEBUG
from ffmeta.utils import epochalypse_now

app = create_app(debug=DEBUG)


if __name__ == '__main__':
    # Configure logging (save 10mb of logs in chunks of 1mb)
    handler = RotatingFileHandler('api.log', maxBytes=1024 * 1024, backupCount=10)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("[{}] App launched.".format(epochalypse_now()))
    app.run(threaded=True)