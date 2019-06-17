#program to retrieve the tweets from github and filter add sentiment then scale, merge and add weight
#execution time depends on network speed and dates to fetch
#import neccessary packages
import pandas as pd
from datetime import datetime
from datetime import timedelta
import csv,re,time,os
import preprocessor as p
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import numpy as np

#inputs to the function
datenow= datetime.now().date()
date=input("enter the date:(2019-05-30)")
#date = "2019-06-04"
company=input("enter the name of the company:(cisco)")
#company="cisco"
header=['Id','Text','Date','Time','Followers count']

#changing to datetime format and fetching first data
print("\ncollecting tweets from each date...\n")
date=datetime.strptime(date,"%Y-%m-%d").date()
url="https://raw.githubusercontent.com/d4datas/twitterdata/master/"+str(company)+"-final-"+str(date)+".csv"
df=pd.read_csv(url,sep='\^',error_bad_lines=False,names=header,usecols = ['Id','Text','Date','Followers count'],skiprows='1',engine='python')

#iterately collect data till yesterday and concatenate
datenow=datenow-timedelta(days=1)
while date<datenow:
	print(date)
	date=date+timedelta(days=1)
	url="https://raw.githubusercontent.com/d4datas/twitterdata/master/"+str(company)+"-final-"+str(date)+".csv"
	df1=pd.read_csv(url,sep='\^',error_bad_lines=False,names=header,usecols = ['Id','Text','Date','Followers count'],skiprows='1',engine='python')
	df = pd.concat([df, df1], ignore_index=True)

#delete dulpicates in terms of id and text
df.drop_duplicates(subset ='Id',keep = False, inplace = True)
df.drop_duplicates(subset = 'Text',keep = False, inplace = True)

#changing date to common format(optional)
#df['Date'] = pd.to_datetime(df['Date'])
#df['Date'] = df['Date'].dt.date

#preprocessing and replacing text from each row using re and preprocessor
print("starting preprocessing of each row...\n")
time.sleep(2)
for j, tweet_text in df.iterrows():
	print(j)
	tweet_text = df.at[j,'Text']
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
	tweet_text = p.clean(tweet_text)
	sen =tweet_text.split(" ")
	lsen =[]
	for i in sen:
		if "/" not in str(i):
			lsen.append(i)

	tweet_text= " ".join(lsen)
	tweet_text.lstrip()
	df.at[j,'Text'] = tweet_text
df.drop_duplicates(subset = 'Text',keep = False, inplace = True)
#print(df)
#df.to_csv("csco_filtered.csv")

#sentiment analysis starts
analyser = SentimentIntensityAnalyzer()
print("\nanalysing sentiment for each date data...\n")
#extracting the dates to iterate
dates = df['Date'].unique().tolist()
#print("list created")
f= open('sentiment_data.csv', 'a')
f.write("Date,negative,positive,neutral,compound,subjectivity,polarity\n")
f.close()

def calcualte_senti(data,df):
	date =data
	mask = (df['Date'] == str(date))
	df = df.loc[mask]
	total_rows=1

	sum_pos=sum_neu=sum_pol=sum_sub=sum_comp=sum_neg=0
	f= open('sentiment_data.csv', 'a')
	sen_writer = csv.writer(f)
	for text in df['Text']:
			total_rows=total_rows+1
			vad = analyser.polarity_scores(text)
			analysis = TextBlob(text)
			pol=round(analysis.polarity,4)
			sub = round(analysis.subjectivity,4)
			sum_neg=sum_neg+vad['neg']
			sum_pos=sum_pos+vad['pos']
			sum_neu=sum_neu+vad['neu']
			sum_comp=sum_comp+vad['compound']
			sum_pol=sum_pol+pol
			sum_sub=sum_sub+sub

	#finding weighted values		
	#print(sum_neg)
	neg_val=sum_neg/total_rows
	pos_val=sum_pos/total_rows
	neu_val=sum_neu/total_rows
	sub_val=sum_sub/total_rows
	pol_val=sum_pol/total_rows
	comp_val = sum_comp/total_rows
	sum_neg=sum_pos=sum_neu=sum_pol=sum_sub=sum_comp=0

	#appending to csv
	f.write(','.join([str(date)+","+str(neg_val)+","+str(pos_val)+","+str(neu_val)+","+str(comp_val)+","+str(sub_val)+","+str(pol_val)])+'\n')
	f.close()	
	#print(str(date)+","+str(neg_val)+","+str(pos_val)+","+str(neu_val)+","+str(comp_val)+","+str(sub_val)+","+str(pol_val))

for date in dates:
	print(".")	
	calcualte_senti(date,df)

#dropping unwanted raws
df = pd.read_csv("sentiment_data.csv",error_bad_lines=False)
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d', errors='coerce')
df = df[pd.notnull(df['Date'])]
#print(df)

#removing temporary file
os.remove("sentiment_data.csv")

#scaling the data using minmax method to 0.8-1.2 range
print("\nscaling data...\n")
time.sleep(2)
#OldRange = (OldMax - OldMin)
oldrange = 1.5
oldmin = -.5
newmin=.8
#NewRange = (NewMax - NewMin) 
newrange = 0.4 
l=[]
for data in df['compound']:
	#NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin
	newvalue = (((data - oldmin) * newrange) / oldrange) + newmin
	print(str(data)+'====>'+str(newvalue))
	l.append(newvalue)
df['sentiment']=l
#print(df)
#df1.to_csv('scaledsentiment.csv')

dfstk = pd.read_csv("CSCO.csv",error_bad_lines=False)
#print(dfstk)

#merging sentiment data and stock data
print("merging data...\n")
time.sleep(2)
df['Date'] = pd.to_datetime(df['Date'])
dfstk['Date'] = pd.to_datetime(dfstk['Date'])
dfmrg = pd.merge(df, dfstk, on="Date")
#print(dfmrg)
#dfmrg.to_csv("sentistock.csv")
#creating a copy with needed columns (adjust for needed columns)
dfnl = dfmrg[['Date','Open','High','Low','Volume','Close','Adj Close','sentiment']].copy()

#adding weighted value to the dataframe
print("adding weightage...\n")
time.sleep(2)
dfnl['weight_value']=dfnl['Close']*dfnl['sentiment']
dfnl['weight_adjusted_close'] = dfnl['Adj Close'] * dfnl['sentiment'] 
print(dfnl)
#dfnl.to_csv("final_data.csv")