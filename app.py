from flask import Flask, render_template, request, jsonify
from twilio.rest import TwilioRestClient
from twilio import twiml
from credentials import settings
import requests
from flaskext.mysql import MySQL

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

# Handles receiving a web message
@app.route('/api/chat/receive', methods=['GET'])
def process_message():
	text = request.values.get('text')
	# get the sentiment
	# Decide how to proceed
	return jsonify({'text': text})
