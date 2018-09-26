import flask
from flask import Flask, Response, Blueprint

def create_app(config_filename):
	
	app = Flask(__name__)
	app.config.from_object(config_filename)
	
	from app.view_facebook import restBP
	from app.view_test import testBP
	from app.view_conversation import conversationBP
	
	app.register_blueprint(restBP)
	app.register_blueprint(testBP)
	app.register_blueprint(conversationBP)
	
	return app