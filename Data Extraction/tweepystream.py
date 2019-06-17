#Final code for Data extraction using tweepy and firestore
#Text preprocessing included
#sentiment analyser embedded
#immune to connectionerror

import tweepy
import csv
import sys,re,os
import datetime,requests
from requests.exceptions import ConnectionError
from time import sleep
import preprocessor as p
import unicodedata
from unidecode import unidecode
from textblob import TextBlob
import pytz

date = datetime.datetime.now().strftime("%Y-%m-%d")

#twitter developer authentication
consumer_key = 'enter consumer_key'
consumer_secret = 'enter consumer_secret key'
access_token = 'enter access_token'
access_token_secret = 'enter access_token_secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#extra function for emoji
def deEmojify(inputString):
	returnString = ""

	for character in inputString:
		try:
			character.encode("ascii")
			returnString += character
		except UnicodeEncodeError:
			replaced = unidecode(str(character))
			if replaced != '':
				returnString += replaced
			else:
				try:
					 returnString += unicodedata.name(character)
				except ValueError:
					 returnString += "x"

	return returnString

p.set_options(p.OPT.MENTION)


#query
search_text ='cisco'



while True :
	url='http://www.google.com/'
	timeout=5
	try:
		some = requests.get(url, timeout=timeout)
		print("Accessing "+search_text+" Data...")
		val= True

	except requests.ConnectionError:
		print("İnternet connection failed.")
		val= False
	if val == True:
		try :
			#create an object called 'customStreamListener'
			class CustomStreamListener(tweepy.StreamListener):
				def on_status(self, status):
					sleep(2)
					n=1
					
					if n==1:
						try:
							tweet_text=status.extended_tweet["full_text"]
							
						except AttributeError:
							tweet_text=p.clean(status.text)
						   
						#initializing database variables
						tweet_text = p.clean(tweet_text)
						tweet_text = deEmojify(tweet_text)
						tweet_text= re.sub(',', ' ', tweet_text)
						sentence =tweet_text.lower() #convert to lower case
						fsen = re.sub(" #| &amp; |\n|\t"," ",sentence) #removing hastags line breaks and tabs with space
						fsen = re.sub("#| \n| \t|\.","",fsen)  #removing hastags line breaks and tabs without space
						fsen = re.sub(r'\d+', '', fsen) #removing numbers
						#removing links from text
						sen =fsen.split(" ")
						lsen=[]
						for i in sen:
							if "https://" not in str(i):
								lsen.append(i)
						tweet_text= " ".join(lsen)

						tweet_id =status.id
						tweet_timestamp = str(status.created_at)
						user_follower_count = status.user.followers_count
						
						gmt_date =datetime.datetime.strptime(tweet_timestamp, '%Y-%m-%d %H:%M:%S')
						eastern = pytz.timezone('US/Eastern')
						fmt = '%d-%m-%Y'
						fmt1 = '%H:%M:%S'
						#textblob
						analysis = TextBlob(tweet_text)
						pol=analysis.polarity
						sub = analysis.subjectivity
						print("textblob:pol="+str(pol)+"sub="+str(sub))
						date=gmt_date.strftime(fmt)
						time = gmt_date.strftime(fmt1)


						print(str(tweet_id)+'==> '+tweet_text)
						with open("output/cisco-final-"+str(date)+".csv", mode='a') as tweets_file:
							tweet_writer = csv.writer(tweets_file, delimiter='^', quotechar='"', quoting=csv.QUOTE_MINIMAL)
							createnew =str(tweet_id)+ '^'+'\''+str(tweet_text)+'\''+ '^' + str(date)+ '^'+str(time)+'^'+ str(user_follower_count)+'^'+str(round(pol,3))+'^'+str(round(sub,3))
							tweet_writer.writerow([createnew])


					   
					 

				def on_error(self, status_code):
					print("error in last on error")
					return True # Don't kill the stream

				def on_timeout(self):
					print("error on last on timeout")
					return True # Don't kill the stream

			
			streamingAPI = tweepy.streaming.Stream(auth, CustomStreamListener(),tweet_mode='extended')
			streamingAPI.filter(track=[search_text],languages=['en'])
		except Exception as e :
			print("Internet connection broke in between transaction")
			print(e)
			sleep(10)
	else :
		print ("Executing sleep")
		sleep(10)
