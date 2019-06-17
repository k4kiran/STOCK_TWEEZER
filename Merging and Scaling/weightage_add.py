import pandas as pd
import numpy as np 

df3 = pd.read_csv('sentistock.csv',usecols=['Date','Open','High','Low','Volume','Close','Adj Close','sentiment'])

df3['weight_value']=df3['Close']*df3['sentiment']
df3['weight_adjusted_close'] = df3['Adj Close'] * df3['sentiment'] 
print(df3)
df3.to_csv("msft_weighted10-18.csv")