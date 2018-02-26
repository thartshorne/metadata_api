FROM python:2.7

# Install MySQL client
RUN apt-get update
RUN apt-get install -y libmysqlclient-dev

# Install app
RUN pip install --upgrade setuptools
WORKDIR /app
ADD requirements.txt /app/requirements.txt
RUN cd /app; pip install -r requirements.txt
ADD . /app

# Configure app
ENV APP_CONFIG=config.cfg

# Run app
EXPOSE 5000
CMD ["python", "/app/webMetadataAPI.py"]
