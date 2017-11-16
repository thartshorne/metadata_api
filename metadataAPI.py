import subprocess
import json
import sys
import os

def selectMetadata(varName, fieldName=None):
	if fieldName == None:
		os.system("php selectMetadata.php " + varName)
	else:
		os.system("php selectMetadata.php " + varName + " " + fieldName)

def filterMetadata(filterD=None):
	if filterD == None:
		os.system("php filterMetadata.php")
	else:
		os.system("php filterMetadata.php " + "\'" + json.dumps(filterD) + "\'")

def searchMetadata(query=None, fieldName=None, searchBody=None):
	if fieldName == None:
		return "[]"
	if query == None:
		os.system("php searchMetadata.php")
	elif searchBody == None:
		os.system("php searchMetadata.php " + "\'" + query + "\'" + " " + fieldName)
	else:
		os.system("php searchMetadata.php " + "\'" + query + "\'" + " " + fieldName + " " + searchBody)


# selectMetadata("p6g23", "varlab")
# d = {"group":"1966"}
# filterMetadata(d)
# searchMetadata("policing", "topic1")
# searchMetadata("m", "respondent", "policingResults.txt")