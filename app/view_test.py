import flask, json
import os
from utils import post_facebook_message, get_weather
from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource

testBP = Blueprint('test', __name__)

api = Api(testBP, prefix='/test')

class TestEndpoint(Resource):
	def __init__(self):
		self.vcap = json.loads(os.environ['VCAP_SERVICES'])

	def get(self):
		return make_response(json.dumps(self.vcap, indent=2))
		
api.add_resource(TestEndpoint, '/')