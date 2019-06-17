import pandas as pd 

df = pd.read_csv('msft_sentiment_10-19.csv')
df1 = pd.read_csv('msft_sentiment_10-19.csv')
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
	#df2['minmax']=str(newvalue)
	l.append(newvalue)
	#print(newvalue)
#print(l)
df1['sentiment']=l
print(df1)
df1.to_csv('scaledsentistock.csv')
#print(df2)
#print(df1)