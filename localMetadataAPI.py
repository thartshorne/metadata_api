# from collections import OrderedDict
# varDict = OrderedDict()
# orderedVars = collections.orderedDict(varDict)
import csv
import sys  

reload(sys)  
sys.setdefaultencoding('latin1')
import json
class Metadata:
	def __init__(self, filename=None):
		self.metadataDict = {}
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
						self.metadataDict[varDict['new_name']] = varDict
					first +=1
		except IOError:
			return 'Error: Unable to read file'

	def select(self, varName, fieldName=None):
		if fieldName is None:
			try:
				fullVar = self.metadataDict[varName]
				return json.dumps(fullVar)
			except KeyError: return '[]'

		if fieldName not in self.fieldNames:
			return ('Error: Invalid field name')
		try:
			varField = self.metadataDict[varName][fieldName]
			return json.dumps(varField)
		except KeyError: return '[]'

	def filter(self, filters=None):
		if filters is None:
			results = []
			for variable in self.metadataDict:
				v = json.dumps(self.metadataDict[variable], ensure_ascii=False)
				results.append(v)
			return results
		for field in filters:
			if field not in self.fieldNames:
				return 'Error: Invalid field name(s)'

		filteredList = []
		for variable in self.metadataDict:
			switch = 0
			for field, value in filters.iteritems():
				if self.metadataDict[variable][field] != value:
					switch = 1
			if switch == 0:
				v = json.dumps(self.metadataDict[variable], ensure_ascii=False)
				filteredList.append(v)
		if filteredList == []:
			return "[]"
		return filteredList

	def search(self, query, searchBody = None):
		if searchBody is None:
			searchBody = self.metadataDict
		else:
			searchList = {}
			for variable in searchBody:
				variable = json.loads(variable, encoding='latin1')
				searchList[variable['new_name']] = variable
			searchBody = searchList

		searchResults = []
		for variable in searchBody:
			if query in searchBody[variable]['varlab'] or query in searchBody[variable]['topic1'] or query in searchBody[variable]['topic1'] or query in searchBody[variable]['q_group_list']:
				v = json.dumps(searchBody[variable], ensure_ascii=False)
				searchResults.append(v)
		if searchResults == []:
			return "[]"
		return searchResults








# m = Metadata()
# # filters = {"wave": "1"}
# # result = m.filter(filters)
# print m.search("policing")
# filters = {"wave": "1", "respondent": "f"}
# print m.filterMetadata(filters)
# print m.selectMetadata('cd3whenint', 'topic_1')
# print m.metadataDict['cd3whenint']
# def helloWorld():
#     return "Hello World!"