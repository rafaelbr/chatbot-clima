import flask, json
import os
from utils import post_facebook_message, get_weather
from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from cloudant_server import DatabaseAccess

conversationBP = Blueprint('conversation', __name__)

api = Api(conversationBP, prefix='/conversation')

class MessagesEndpoint(Resource):
	def __init__(self):
		self.database = DatabaseAccess()		
	
	def get(self):
		return make_response(json.dumps(list(self.database.listConversations())))
		
api.add_resource(MessagesEndpoint, '/messages')