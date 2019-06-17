from bs4 import BeautifulSoup
import requests

tick = input("Enter the ticker of the company(in caps):")
page = requests.get("https://in.finance.yahoo.com/quote/"+str(tick)+"/history?p="+str(tick))

soup = BeautifulSoup(page.content, 'html.parser')
data = soup.find('tr', class_= "BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)")
l = []
for i in data:
    #print(i.get_text())
    l.append(i.get_text())
    #print("\n")

date = l[0]
op = l[1]
high = l[2]
low = l[3]
close = l[4]
adj_cl = l[5]
vol = l[6]

print("date:"+date+"\nop:"+op+"\nhigh:"+high+"\nlow:"+low+"\nclose:"+close+"\nadj:"+adj_cl+"\nvol:"+vol+"\n")
