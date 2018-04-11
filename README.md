# Fragile Families Metadata API Repository

[![Build Status](https://travis-ci.org/fragilefamilieschallenge/metadata_api.svg?branch=master)](https://travis-ci.org/fragilefamilieschallenge/metadata_api)


localMetadataAPI.py is a local library that contains all logic to select, filter, and search the metadata within a python project

webMetadataAPI.py is a python flask app that allows server requests to be passed to the local API to provide select, filter, and search functions from the web

FFMetadata20171101.csv is the unmodified metadata CSV file
	-CSV version is not recommended because the file text contains commas which creates conflict

FFMetadata20171101_tab.txt is a tab separated version of the metadata file and is the recommended file for further work
