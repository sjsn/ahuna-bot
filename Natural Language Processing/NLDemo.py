import Algorithmia
from random import randint
from chatterbot import ChatBot

chatbot = ChatBot(
    'Ahuna',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer'
)

chatbot.train("chatterbot.corpus.english.conversations")

apiKey = 'simwZCh9tS6b81wSwLtrdIauZhi1'
client = Algorithmia.client(apiKey)
algo = client.algo('StanfordNLP/Lemmatizer/0.1.0')
algo2 = client.algo('nlp/SentimentAnalysis/0.1.2')
algo3 = client.algo('nlp/AutoTag/1.0.0')

input = "My day was okay."
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
} # Determines which group the message belongs to
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

con = algo.pipe(input)
print con.result

response = algo2.pipe(input)
result = response.result

if (result >= 3): # Good to great
	print "Glad to hear that you are doing good!"
elif (result == 2): # Okay or Conversational
	print(chatbot.get_response(input))
else: # Poor to extremely bad
	tags = algo3.pipe(con.result)
	for a in tags.result:
		for x in mainTags:
			for y in mainTags[x]:
				if (a == mainTags[x][y]):
					rand = randint(0, 1)
					print resources[x][rand]['data']

"""

	Cases: 
	1. Panic Attack
	2. Suicide
	3. Breaking Up w/ Significant Other

	TODO:
	1. Add in the predetermined response for when something good happens.
	2. Ask if it helped, ask them to respondwith yes or no.

 """


# convert words to connonical form
# run through ML to determine the setiment of the the message
# if poor setament, then run through tagging
# after finding tags, search database for resources based on given tags
	# if tag is found, then return content
	# if tag is not found, send basic sentiment - asking them to help contribute.