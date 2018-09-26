import flask, json, os
import config, datetime
from contexthandler import ContextHandler
from cloudant_server import DatabaseAccess
from utils import post_facebook_message, get_weather
from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from watson_developer_cloud import AssistantV1

import random

restBP = Blueprint('facebook', __name__)

api = Api(restBP, prefix='/facebook')

class FacebookEndpoint(Resource):
	def __init__(self):
		self.vcap_services = json.loads(os.environ['VCAP_SERVICES'])
		self.assistant = AssistantV1(
			url = self.vcap_services['conversation'][0]['credentials']['url'],
			iam_api_key = self.vcap_services['conversation'][0]['credentials']['apikey'],
			version = '2018-07-10'
		)
		self.contexthandler = ContextHandler()
		self.database = DatabaseAccess()

	def get(self):
		token = request.args.get('hub.verify_token')
		if token == config.FACEBOOK_VERIFY_TOKEN:
			return make_response(request.args.get('hub.challenge'))
		else:
			return make_response('Invalid token')
			
	def post(self):
		incoming_message = request.get_json(force=True)
		
		for entry in incoming_message['entry']:
			for message in entry['messaging']:
				if 'message' in message:
					print(message)
					sender_id = message['sender']['id']
					text_message = message['message']['text']
					#recupero contexto atual de acordo com o sender_id do facebook
					if sender_id in self.contexthandler.contextmap:
						context = self.contexthandler.contextmap[sender_id]
					else:
						context = {}
						
					#envio mensagem para o Watson Assistant
					response = self.assistant.message(
						workspace_id = config.WATSON_ASSISTANT_WORKSPACE_ID,
						input = {
							'text': text_message
						},
						context = context	
					)
					
					#salvo contexto do assistant de acordo com o sender_id
					self.contexthandler.contextmap[sender_id] = response['context']
					
					#verifico se existe intents, se sim, pego a primeira
					if len(response['intents']) > 0:
						intent = response['intents'][0]['intent']
					#verifico se existe entities, se sim, verifico se eh uma sys-date, se for, pego a data
					if len(response['entities']) > 0 and response['entities'][0]['entity'] == 'sys-date':
						date = response['entities'][0]['value']
					
					if response['output']['text']:
        				#se a intent for weather, pego a resposta e coloco o clima do dia nela
						if intent == 'weather' and date != '':
							r = response['output']['text'][0]
							r = r.format(get_weather(date))
							text = r
						#se nao, envio a resposta direta
						else:
							text = response['output']['text'][0]
					
					#envio texto para o facebook
					post_facebook_message(sender_id, text)
					
					#mensagem de log a ser gravada no banco de dados
					log_message = {
						'date': str(datetime.datetime.now()),
						'input': text_message,
						'output': text
					}
					self.database.save(log_message)
		
api.add_resource(FacebookEndpoint, '/message')