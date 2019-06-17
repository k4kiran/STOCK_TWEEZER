import pandas as pd 
import csv
import re
import time
import datetime
import preprocessor as p

#datesince = "2019-02-02"
#date_time_obj = datetime.datetime.strptime(datesince, '%Y-%m-%d').date()
for i in range(0,1):
	##date_time_obj_tomorrow = date_time_obj+datetime.timedelta(days=1)
	#print("today:"+str(date_time_obj))
	#print("tomorrow:"+str(date_time_obj_tomorrow))
	#p.set_options(p.OPT.MENTION,p.OPT.URL)
	filenam = "cisco_final.csv"
	#header=['Id','Text','Date','Time','Followers count']
	df = pd.read_csv(filenam,error_bad_lines=False,usecols = ['date','text'],skiprows='1',engine='python')
	df['date'] = pd.to_datetime(df['date'])
	df['date'] = df['date'].dt.date
	#print(df['date']) 
	print("date checkpoint reached")

	for j, tweet_text in df.iterrows():
		print(j)
		tweet_text = df.at[j,'text']
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
					#lsen.append(i)
					if "http://" not in str(i):
						lsen.append(i)
		tweet_text= " ".join(lsen)
		#print(tweet_text)
		tweet_text = p.clean(tweet_text)
		sen =tweet_text.split(" ")
		lsen =[]
		for i in sen:
			if "/" not in str(i):
				#lsen.append(i)
				lsen.append(i)

		tweet_text= " ".join(lsen)
		tweet_text.lstrip()
		#print(lsen)
		#tweet_text = re.sub('</*>', ' ', tweet_text)
		#tweet_text = deEmojify(tweet_text)
		#print(tweet_text)
		df.at[j,'text'] = tweet_text
		#df.drop_duplicates(subset ='Id',keep = False, inplace = True)
	df.drop_duplicates(subset = 'text',keep = False, inplace = True)
	#print(df)
	#print(df)
	#date_time_obj = date_time_obj+datetime.timedelta(days=1)
	df.to_csv("csco_filtered.csv")
	print("csv file created successfully for ")

#print(df)
