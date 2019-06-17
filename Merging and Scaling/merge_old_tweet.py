#program to merge the tweets from
import pandas as pd
from datetime import datetime
from datetime import timedelta
#string=[]
#generate today time
#datenow= datetime.now().date()
#print(datenow)
#date3=input("enter the date:(2019-04-17)")
date3 = "2010-01-01"
#company=input("enter the name of the company")
#header=['Id','Text','Date','Time','Followers count']

date3=datetime.strptime(date3,"%Y-%m-%d").date()
url="oldtweet/cisco_"+str(date3)+".csv"
sort_by_time=pd.read_csv(url,error_bad_lines=False,usecols = ['date','text'],skiprows='1',engine='python')
sort_by_time['date'] = date3
id = 36536765435
sort_by_time['id'] = id
#sort_by_time = val.sort_values('Date',ascending=False)
#sort_by_time.drop_duplicates(subset ='Id',keep = False, inplace = True)

#datenow=datenow-timedelta(days=1)
#for i in range(0,5):

for i in range(0,2853):
	print(i,date3)
	id = id+1
	#print(date3)
	date3=date3+timedelta(days=1)
	url="oldtweet/cisco_"+str(date3)+".csv"
	sort_by_time1=pd.read_csv(url,error_bad_lines=False,usecols = ['date','text'],skiprows='1',engine='python')
	sort_by_time1['date'] = date3
	sort_by_time1['id'] = id
	#sort_by_time1 = val1.sort_values('Date',ascending=False)
	#sort_by_time1.drop_duplicates(subset ='Id',keep = False, inplace = True)
	sort_by_time = pd.concat([sort_by_time, sort_by_time1], ignore_index=True)

#sort_by_time.drop_duplicates(subset ='Id',keep = False, inplace = True)
sort_by_time.drop_duplicates(subset = 'text',keep = False, inplace = True)
print(sort_by_time)
sort_by_time.to_csv("cisco_2010-17.csv")
#sort_by_time.to_csv("new1.csv")
