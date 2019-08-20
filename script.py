'''
This Python script uses Twurl, they twitter curl implementation of it's API
to Tweet(Post) random quotes from brainyquote.com
'''
import os
import random
import requests
import urllib.request
import time
from datetime import datetime
from bs4 import BeautifulSoup
import json

#check if tweet alread exists in the DB, if so return True else return False
def tweetExists(input):

	with open('./tempDB.json') as myfile:

		data = json.load(myfile)

		storedTweetID = data['id'][0]
		print(storedTweetID)

		if (input == storedTweetID):
			return True
		else:
			return False

#reacts to tweets tweeted to the bot account
#tweets read by bot are in the form of @MarioDevs #MotivateMe / #Space / #Stocks
def reactToTweet():

	#uses the twitter API to get and store a json file of this accounts timeline
	os.system('twurl \"/1.1/statuses/mentions_timeline.json?count=1\" > result.json')

	#open the json file, parse, and performs an action depending on tweet
	with open('./result.json') as myfile:

		data = json.load(myfile)

		#check if this bot has been tweeted to
		if ('@MarioDevs' in data[0]['text']):

			humanUser = "@" + data[0]['user']['screen_name']
			tweetID = data[0]['id']

			#if tweet already exists in the DB then do nothing, else determine what tweet info tweet wants
			if (tweetExists(tweetID) == True):

				print('Already Replied to ' + humanUser)

			else:

				outputID = {}
				outputID['id'] = [tweetID]
				#save new tweet to DB for future reference
				with open('tempDB.json', 'w') as outfile:
					json.dump(outputID, outfile)
				#print(json.dumps(data, indent=4))

				#check what the hashtag is asking for and react to it
				if ('#MotivateMe' in data[0]['text']):

					message = humanUser + " " + scrapeQuote()
					
					tweet(message)

					print("Replied to " + humanUser)

				elif ('#Space' in data[0]['text']):
					print("#Space")

				elif ('#Stocks' in data[0]['text'] or '#Stock' in data[0]['text']):

					string = data[0]['text'].split(' ')[1]

					stockName = string[7:]

					print(stockName)

					result = scrapeStock(str(stockName))

					if (result == 'Error'):

						print("Can't Tweet, Error with Incoming Tweet!")

					else:

						message = humanUser + "\n" + result

						tweet(message)

						print("Replied to " + humanUser)


				else:
					print('Hashtag Not Known')
		else:
			print('@MarioDevs Not Mentioned')

#scrapes a quote website for a random quote and tweets it
def scrapeQuote():

	#generates a random number which will correspond to a list of quotes fetched
	num = random.randint(0, 20)
	#url of quote DB
	url = 'https://www.brainyquote.com/topics/daily'
	#response from the curl call, request is similar to curl
	response = requests.get(url)
	#cleans up the response
	soup = BeautifulSoup(response.text, "html.parser")
	#creates a list of quotes and authors, relationship is 1 to 1
	listOfQuotes = soup.findAll(title="view quote")
	listOfAuthors = soup.findAll(title="view author")
	#filters out the quote and the corresponding author string
	quote = listOfQuotes[num].string
	author = '-' + listOfAuthors[num].string
	#concatenated quote and author
	message = quote + '\n' + author
	print(message)

	return message

def scrapeStock(stockName):

	name = stockName.lower()

	url = 'https://www.nasdaq.com/symbol/' + name + '/real-time'

	response = requests.get(url)

	soup = BeautifulSoup(response.text, "html.parser")

	try:

		currPrice = soup.find("div", id="qwidget_lastsale").string

		netChange = soup.find("div", id="qwidget_netchange").string

		changePercent = soup.find("div", id="qwidget_percent").string

		sign = soup.find("div", id="qwidget_netchange")

		if ('Green' in sign):

			netChange = '+' + netChange
			changePercent = '+' + changePercent

		else:

			netChange = '-' + netChange
			changePercent = '-' + changePercent


		message = 'Name: ' + stockName.upper() + '\n' + \
				  'Current Price: ' + currPrice + '\n' + \
				  'Net Change: ' + netChange + '\n' + \
			  	  'Percent Change: ' + changePercent

		print(message)

		return message
		
	except Exception as e:

		print("Error")

		return "Error"


def scrapeSpace():

	url = 'https://www.nasa.gov/news/releases/latest/index.html'

	response = requests.get(url)

	soup = BeautifulSoup(response.text, "html.parser")



	return 2


#calls the Twitter API and performs a Tweet 
def tweet(input):

	#cleans the string and removes and single quotes so Twitter API does not throw an error 
	cleanStr = ''
	i = 0
	while i < len(input):

		if input[i] != '\'':
			cleanStr = cleanStr + input[i]

		i = i + 1

	#this output quiets the json response from twitter
	os.system('twurl -q -d \'status=' + cleanStr + '\' /1.1/statuses/update.json')

#the main function
def main():

	#reactToTweet()
	#scrapeStock('TSLA')

	#scrapeStock('GOOGL')


	while True:

		reactToTweet()

		time.sleep(10)


#calls the main
if __name__=="__main__":
	main()
