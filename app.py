from flask import Flask, render_template, request, jsonify
from twilio.rest import TwilioRestClient
from twilio import twiml
from credentials import settings
import requests

app = Flask(__name__)

client = TwilioRestClient(settings['sid'], settings['auth'])


nums = {}
twilio_number = '(253) 343-9145'

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

@app.route('/')
def hello():
	return render_template('index.html')

@app.route('/api/receive', methods=['POST'])
def recieve_sms():
	from_number = requests.values.get('From', None)
	from_msg = requests.values.get('Body', None)
	nums[from_number].append(from_msg)
	res = twiml.Response()
	res.message("Got your message!")
	return str(res)

@app.route('/api/messages/', methods=['GET', 'POST'])
def show_messages():
	if len(nums) == 0:
		return "No messages. Send one to " + twilio_number + " to start!"
	else:
		return flask.jsonify(nums)

@app.route('/api/chat/receive', methods=['GET'])
def process_message():
	text = request.args.get('text')
	# get the sentiment
	# Decide how to proceed
	return jsonify({'text': text})