Fragile Families Metadata API Repository

metadataAPI.php is the main logic file which can be used to embed and access the entire API from within a PHP project or from the command line.

metadataAPI.py is the python script that creates subproccesses for all of the API functions from selectMetadata.php, filterMetadata.php and searchMetadata.php. This serves as a python module to embed and access the API from a python project.

selectMetadata.php returns a specific field of a given variable, or the entire variable if no field is specified

filterMetadata.php returns a list of JSON objects given a set of filter values (in JSON format) for variable categories, or the entire set of metadata if no filters are provided

searchMetadata.php returns a list of JSON objects given a query string and a search category, or the entire set of metadata if query is empty