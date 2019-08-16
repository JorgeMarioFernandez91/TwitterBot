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

#scrapes a quote website for a random quote and tweets it
def scrapeQuote():

	#generates a random number which will correspond to a list of quotes fetched
	num = random.randint(1, 20)
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

	#tweets the message
	tweet(message)

#calls the Twitter API and performs a Tweet 
def tweet(input):

	#cleans the string and removes and single quotes so Twitter API does not throw an error 
	cleanStr = ''
	i = 0
	while i < len(input):

		if input[i] != '\'':
			cleanStr = cleanStr + input[i]

		i = i + 1

	#this output prints out the json response from twitter to stdout
	#output = 'twurl -d \'status=' + input + '\' /1.1/statuses/update.json'

	#this output quiets the json response from twitter
	output = 'twurl -q -d \'status=' + cleanStr + '\' /1.1/statuses/update.json'
	os.system(output)

#the main function
def main():

	while True:
		#get time 
		currTime = datetime.now()
		hour = currTime.hour
		minute = currTime.minute
		second = currTime.second

		#Tweet every hour
		if (minute % 30 == 0):
			scrapeQuote()
			print("Tweet Tweeted!")

		if (minute < 30):
			remaining = 30 - int(minute)
		else:
			remaining = 60 - int(minute)

		print("Waiting... " + str(remaining) + " minute(s) until next Tweet")
		#sleep for a minute
		time.sleep(60)

#calls the main
if __name__=="__main__":
	main()

