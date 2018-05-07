import logging
from logging.handlers import RotatingFileHandler

from ffmeta import create_app
from ffmeta.settings import DEBUG
from ffmeta.utils import epochalypse_now

application = create_app(debug=DEBUG)


if __name__ == '__main__':
    # Configure logging (save 10mb of logs in chunks of 1mb)
    handler = RotatingFileHandler('api.log', maxBytes=1024 * 1024, backupCount=10)
    handler.setLevel(logging.INFO)
    application.logger.addHandler(handler)
    application.logger.setLevel(logging.INFO)
    application.logger.info("[{}] App launched.".format(epochalypse_now()))
    application.run(threaded=True)