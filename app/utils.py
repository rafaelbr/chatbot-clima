import json, requests, config, datetime

#funcao que posta mensagem no facebook de acordo com o id do sender
def post_facebook_message(fbid, message):
	post_url = 'https://graph.facebook.com/v2.6/me/messages?access_token={}'.format(config.FACEBOOK_ACCESS_TOKEN)
	response_msg = json.dumps(
		{
			'recipient': {'id': fbid},
			'message': {'text': message}
		}		
	)
	status = requests.post(post_url, headers={'Content-Type': 'application/json'}, data=response_msg)
	print(status.json)
	

#funcao que recupera dados da url e pega o dia de acordo com a data de hoje. 
def get_weather(date):
	#weather underground - clima de Brasilia para 10 dias a frente
	url = 'http://api.wunderground.com/api/3a1bac903d7ec325/geolookup/forecast10day/lang:BR/q/zmw:00000.15.83377.json'

	#calculo quantos dias a partir de hoje, a data informada esta
	date_now = datetime.date.today()
	d = datetime.datetime.strptime(date, '%Y-%m-%d').date()
	diff = d - date_now
    
	response = requests.get(url)
	#existe duas entradas para cada dia, clima durante o dia e durante a noite. Quero pegar
	#o clima durante o dia, por isso pego somente os indices pares
	forecast = response.json()['forecast']['txt_forecast']['forecastday'][diff.days * 2]['fcttext_metric']    
	return forecast