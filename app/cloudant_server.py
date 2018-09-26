import os, json
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

class DatabaseAccess():
	def __init__(self):
		vcap_cloudant = json.loads(os.environ['VCAP_SERVICES'])['cloudantNoSQLDB'][0]['credentials']
		self.cloudant = Cloudant(vcap_cloudant['username'], vcap_cloudant['password'], url=vcap_cloudant['url'])
		self.cloudant.connect()
		self.database = self.cloudant['conversations_watson']
		
	def save(self, data):
		self.database.create_document(data)
		
	def listConversations(self):
		result = Result(self.database.all_docs, include_docs=True)
		return result
			
	def __del__(self):
		self.cloudant.disconnect()