import pandas as pd 
import csv
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

analyser = SentimentIntensityAnalyzer()

df = pd.read_csv("msft_filtered.csv",error_bad_lines=False)
#df['Tweet Date'] = pd.to_datetime(df['Tweet Date'])
dates = df['date'].unique().tolist()
print("list created")
#global sum_neg,sum_pos,sum_neu,sum_pol,sum_sub,sum_comp

# sum_neg=sum_pos=sum_neu=sum_pol=sum_sub=sum_comp=0


def calcualte_senti(data,df):
	# date = input("enter the date(eg:-2018-11-30):")
	date =data
	mask = (df['date'] == str(date))
	df = df.loc[mask]
	total_rows=1

	#sum_neg,sum_pos,sum_neu,sum_pol,sum_sub,sum_comp
	sum_pos=sum_neu=sum_pol=sum_sub=sum_comp=sum_neg=0
	# with open('cisco_sentiment.csv', 'a') as f:
	f= open('msft_sentiment_10-19.csv', 'a')
	sen_writer = csv.writer(f)
	for text in df['text']:
			total_rows=total_rows+1
			# global sum_neg,sum_pos,sum_neu,sum_pol,sum_sub,sum_comp
			#print(text)
			vad = analyser.polarity_scores(text)
			analysis = TextBlob(text)
			pol=round(analysis.polarity,4)
			sub = round(analysis.subjectivity,4)
			#print(vad)
			# print(pol,sub)
			#adding all values
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
	print(date)	
	calcualte_senti(date,df)