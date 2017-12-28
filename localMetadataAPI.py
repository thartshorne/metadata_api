# from collections import OrderedDict
# varDict = OrderedDict()
# orderedVars = collections.orderedDict(varDict)
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
						varDict = {}
						for attr in variable:
							varDict[self.fieldNames[index]] = attr
							index+=1
						self.metadataArray[varDict['new_name']] = varDict
					first +=1
		except IOError:
			print('Error: Unable to read file')

	def select(self, varName, fieldName=None):
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

	def filter(self, filters=None):
		if filters is None:
			results = []
			for variable in self.metadataArray:
				v = json.dumps(self.metadataArray[variable], ensure_ascii=False)
				results.append(v)
			return results
		for field in filters:
			if field not in self.fieldNames:
				return 'Error: Invalid field name(s)'

		filteredList = []
		for variable in self.metadataArray:
			switch = 0
			for field, value in filters.iteritems():
				if self.metadataArray[variable][field] != value:
					switch = 1
			if switch == 0:
				v = json.dumps(self.metadataArray[variable], ensure_ascii=False)
				filteredList.append(v)
		if filteredList == []:
			return "[]"
		return filteredList
