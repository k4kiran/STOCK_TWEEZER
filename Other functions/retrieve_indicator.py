
import requests
import json
import datetime
import pandas as pd
import myfns

data=[]
def indicator(val,tick,per,rng):
    
    page = requests.get("https://www.alphavantage.co/query?function="+str(val)+"&symbol="+str(tick)+"&interval="+str(rng)+"&time_period="+str(per)+"&series_type=close&apikey=LFTWYCZ4Q9ISZRZG")
    x=json.loads(page.content)
    if str(val)=="AD":
        z=x["Technical Analysis: Chaikin A/D"]
    else:
        z=x["Technical Analysis: "+str(val)]
     
    for y in z:
        #print(z[str(y)])
        try:
            date =datetime.datetime.strptime(y, '%Y-%m-%d %H:%M:%S')
        except:
            try:
                date = datetime.datetime.strptime(y, '%Y-%m-%d')
            except:
                date = datetime.datetime.strptime(y, '%Y-%m-%d %H:%M')
        fmt = '%d-%m-%Y'
        date1 = date.strftime(fmt)
        myfns.ifcase1(y,z,date1,val,data)
        
    if(val=="AROON"):
        df = pd.DataFrame(data, columns = ['date','Aroon_Down', 'Aroon_Up'])
        print(df)
        data.clear()
    elif val=="SMA":
        df = pd.DataFrame(data, columns = ['date','SMA'])
        print(df)
        data.clear()
    elif val=="EMA":
        df = pd.DataFrame(data, columns = ['date','EMA'])
        print(df)
        data.clear()
    elif val=="MACD":
        df = pd.DataFrame(data, columns = ['date','MACD','MACD signal','MACD signal'])
        print(df)
        data.clear()
    elif val=="STOCH":
        df = pd.DataFrame(data, columns = ['date','SlowK', 'SlowD'])
        print(df)
        data.clear()
    elif val=="RSI":
        df = pd.DataFrame(data, columns = ['date','RSI'])
        print(df)
        data.clear()
    elif val=="ADX":
        df = pd.DataFrame(data, columns = ['date','ADX'])
        print(df)
        data.clear()
    elif val=="CCI":
        df = pd.DataFrame(data, columns = ['date','CCI'])
        print(df)
        data.clear()
    elif val=="BBANDS":
        df = pd.DataFrame(data, columns = ['date','Real Middle Band', 'Real Upper Band','Real Lower Band'])
        print(df)
        data.clear()
    elif val=="AD":
        df = pd.DataFrame(data, columns = ['date','Chaikin A/D'])
        print(df)
        data.clear()
    elif val=="OBV":
        df = pd.DataFrame(data, columns = ['date','OBV'])
        print(df)
        data.clear()
    
    
        
if __name__=="__main__":
    print("indicators: SMA,EMA,MACD,STOCH,RSI,ADX,CCI,AROON,BBANDS,AD,OBV")
    val = input("enter the indicator name(eg:AROON)(caps):")
    print("tickers:MSFT,NVDA,TSLA,QCOM,INTC")
    tick = input("enter the ticker name(eg:MSFT)(caps):")
    per = input("enter the time perioud(eg:30):")
    rng = input("daily/weekly/monthly ? :")
    print("Retrieving Data...")
    

    indicator(val,tick,per,rng)