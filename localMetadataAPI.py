# from collections import OrderedDict
import csv
import sys
import json
class Metadata:
	def __init__(self, filename=None):
		self.metadataArray = {}
		self.fieldNames = []
		if filename is None:
			filename = "FFMetadata20171101_tab.txt"
		try:
			with open(filename, "rU") as f:
				first = 0
				for line in csv.reader(f, dialect="excel-tab"):
					if first == 0:
						self.fieldNames = line
					else:
						variable = line
						index = 0
						# varDict = OrderedDict()
						varDict = {}
						for attr in variable:
							varDict[self.fieldNames[index]] = attr
							index+=1
						# orderedVars = collections.orderedDict(varDict)
						self.metadataArray[varDict['new_name']] = varDict
					first +=1
		except IOError:
			print('Error: Unable to read file')

	def selectMetadata(self, varName, fieldName=None):
		if fieldName is None:
			try:
				fullVar = self.metadataArray[varName]
				return json.dumps(fullVar)
			except KeyError: return '[]'

		if fieldName not in self.fieldNames:
			return ('Error: Invalid field name')
		try:
			varField = self.metadataArray[varName][fieldName]
			return json.dumps(varField)
		except KeyError: return '[]'


# m = Metadata()
# print m.selectMetadata('cd3whenint', 'topic_1')
# print m.metadataArray['cd3whenint']
# def helloWorld():
#     return "Hello World!"