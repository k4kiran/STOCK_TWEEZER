def aroon(y,z,date1,data):
    Aroon_down = z[str(y)]["Aroon Down"]
    Aroon_up = z[str(y)]["Aroon Up"]
    #print("date="+date1+"\tAroon_Down:"+Aroon_down+"\t"+"Aroon Up:"+Aroon_up+"\n")
    data.append([date1,Aroon_down,Aroon_up])
    

def sma(y,z,date1,data):
    sma1 = z[str(y)]["SMA"]
    data.append([date1,sma1])
    #print("date="+date1+"\tSMA:"+sma1+"\n")

def ema(y,z,date1,data):
    ema1 = z[str(y)]["EMA"]
    data.append([date1,ema1])
    #print("date="+date1+"\tEMA:"+ema1+"\n")

def macd(y,z,date1,data):
    macd1 = z[str(y)]["MACD"]
    macdsig = z[str(y)]["MACD_Signal"]
    macdhist = z[str(y)]["MACD_Hist"]
    data.append([date1,macd1,macdsig,macdhist])

    #print("date="+date1+"\tMACD:"+macd1+"\tMACD SIGNAL:"+macdsig+"\tMACD HIST:"+macdhist+"\n")

def stoch(y,z,date1,data):
    slowk = z[str(y)]["SlowK"]
    slowd = z[str(y)]["SlowD"]
    data.append([date1,slowk,slowd])
    #print("date="+date1+"\tSLOWK:"+slowk+"\t"+"SLOWD:"+slowd+"\n")

def rsi(y,z,date1,data):
    rsi1 = z[str(y)]["RSI"]
    data.append([date1,rsi1])
    #print("date="+date1+"\tRSI:"+rsi1+"\n")

def adx(y,z,date1,data):
    adx1 = z[str(y)]["ADX"]
    data.append([date1,adx1])
    #print("date="+date1+"\tADX:"+adx1+"\n")

def cci(y,z,date1,data):
    cci1 = z[str(y)]["CCI"]
    data.append([date1,cci1])
    #print("date="+date1+"\tCCI:"+cci1+"\n")

def bbands(y,z,date1,data):
    rmb1 = z[str(y)]["Real Middle Band"]
    rub1 = z[str(y)]["Real Upper Band"]
    rlb1 = z[str(y)]["Real Lower Band"]
    data.append([date1,rmb1,rub1,rlb1])
    #print("date="+date1+"\tReal Middle Band:"+rmb1+"\tReal Upper Band:"+rub1+"\tReal Lower Band:"+rlb1+"\n")

def ad(y,z,date1,data):
    ad1 = z[str(y)]["Chaikin A/D"]
    data.append([date1,ad1])
    #print("date="+date1+"\tChaikin A/D:"+ad1+"\n")

def obv(y,z,date1,data):
    obv1 = z[str(y)]["OBV"]
    data.append([date1,obv1])
    #print("date="+date1+"\tOBV:"+obv1+"\n")
def ifcase1(y,z,date1,val,data):
    if val=="AROON":
        aroon(y,z,date1,data)
    elif val=="SMA":
        sma(y,z,date1,data)
    elif val=="EMA":
        ema(y,z,date1,data)
    elif val=="MACD":
        macd(y,z,date1,data)
    elif val=="STOCH":
        stoch(y,z,date1,data)
    elif val=="RSI":
        rsi(y,z,date1,data)
    elif val=="ADX":
        adx(y,z,date1,data)
    elif val=="CCI":
        cci(y,z,date1,data)
    elif val=="BBANDS":
        bbands(y,z,date1,data)
    elif val=="AD":
        ad(y,z,date1,data)
    elif val=="OBV":
        obv(y,z,date1,data)
    else:
        print("invalid choice...")