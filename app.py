from flask import Flask, render_template, request, jsonify
from twilio.rest import TwilioRestClient
from twilio import twiml
from credentials import settings
import requests
from flaskext.mysql import MySQL
import Algorithmia
from chatterbot import ChatBot
from random import randint

# Declares flask app
app = Flask(__name__)

# MySQL setup
# mysql = MySQL()
# mysql.init_app(app)
# cursor = mysql.get_db().cursor()

# For Twilio
client = TwilioRestClient(settings['sid'], settings['auth'])
twilio_number = '(253) 343-9145'

# Changes Jinja's expression blocks so angular can work
jinja_options = app.jinja_options.copy()
jinja_options.update(dict(
    block_start_string='<%',
    block_end_string='%>',
    variable_start_string='%%',
    variable_end_string='%%',
    comment_start_string='<#',
    comment_end_string='#>',
))
app.jinja_options = jinja_options

# Algorithmia setup
apiKey = 'simwZCh9tS6b81wSwLtrdIauZhi1'
client = Algorithmia.client(apiKey)
algo = client.algo('StanfordNLP/Lemmatizer/0.1.0')
algo2 = client.algo('nlp/SentimentAnalysis/0.1.2')
algo3 = client.algo('nlp/AutoTag/1.0.0')

# ChatBot Stuff
chatbot = ChatBot('Ahuna',trainer='chatterbot.trainers.ChatterBotCorpusTrainer')
chatbot.train("chatterbot.corpus.english.conversations")

# Main front-end endpoint
@app.route('/')
def hello():
	return render_template('index.html')

# Handle receiving text messages
@app.route('/api/receive', methods=['POST'])
def recieve_sms():
	from_number = requests.values.get('From', None)
	to_number = requests.values.get('To', None)
	text = requests.values.get('Text', None)
	nums[from_number].append(from_msg)
	res = twiml.Response()
	res.message("Got your message!")
	return str(res)

# Handle sending back text messages
@app.route('/api/messages/', methods=['GET', 'POST'])
def show_messages():
	if len(nums) == 0:
		return "No messages. Send one to " + twilio_number + " to start!"
	else:
		return flask.jsonify(nums)

mainTags = {
 	0: 
 		{
 			0: 'panic attack', 
 			1: 'panic'}, 
 	1: 
 		{
 			0: 'suicide', 
 			1: 'kill'}, 
 	2: 
 		{
 			0: 'break'}
} 
# Determines which group the message belongs to
resources = {
 	0: 
 		{
 			0: {'type': 'url', 'data': 'https://www.lifeline.org.au/Get-Help/Facts---Information/Panic-Attacks/Panic-Attacks'}, 
 		 	1: {'type': 'phone-number', 'data': '800-64-PANIC'}}, 
	1: 
 	 	{
 	 		0: {'type': 'url', 'data': 'http://suicidepreventionlifeline.org/#'}, 
 	 		1: {'type': 'phone-number', 'data': '1-800-273-8255'}},
 	 2: 
 	 	{
 	 		0: {'type': 'url', 'data': 'http://www.7cups.com/how-to-get-over-a-breakup/'}, 
 	 		1: {'type': 'phone-number', 'data': '741-741'}},
 }

# Handles receiving a web message
@app.route('/api/chat/receive', methods=['GET'])
def process_message():
	text = request.values.get('text')
	response = algo2.pipe(text)
	result = response.result
	if (result >= 3): # Good to great
		return jsonify({'text': "Glad to hear that you are doing good!"})
	elif (result == 2): # Okay or Conversational
		res = chatbot.get_response(text).text
	else: # Poor to extremely bad
		con = algo.pipe(text)
		tags = algo3.pipe(con.result)
		for a in tags.result:
			for x in mainTags:
				for y in mainTags[x]:
					if (a == mainTags[x][y]):
						rand = randint(0, 1)
						res = resources[x][rand]['data']
	return jsonify({'text': res})

# Helper function to decide how to proceed with user input based on sentiment
def process_path(text, sentiment):
	if sentiment == 4:
		return "Glad to hear it!"
	elif sentiment == 3:
		return "Tell me more about that."
	elif sentiment == 2:
		return "Do you need to talk about it?"
	else:
		return "Do you need help?"
