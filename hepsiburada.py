import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import smtplib
liste=[]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36"}
recipient = input("enter your mail addr to receive the mail")
sender = input("enter the sender mail")
password = input("enter the sender password")
def proxy(proxy,url):    
    
    try:
        r = requests.get(url,headers=headers,proxies={'http': proxy,'https':proxy},timeout=3)
    except:
        r = requests.get(url,headers=headers)
        print("failed")
    return r

def proxy(url):
    r = requests.get(url,headers=headers)
    return r

def hepsiburada():
    url = input("enter the urls seperated by comma: ")
    urlList = url.split(",")
    for url in urlList:
        
        soup = BeautifulSoup(proxy(url).content,features="lxml") ###### change the proxy parameters if you want to change your proxy in line 27 and 33
        try:
            itemsfull = soup.find('ul',{"class":"productListContent-wrapper productListContent-grid-0"})
            items = itemsfull.find_all('li',{"class":"productListContent-item"})
            for item in items:
                url="https://www.hepsiburada.com/"+(item.a.get("href")) 
                soup = BeautifulSoup(proxy(url).content,features="lxml") ###### change the proxy parameters if you want to change your proxy in line 27 and 33
                theprocess(url,soup)
        except:
            theprocess(url,soup)
def theprocess(url,soup): 
    dataDictionary={"website":"hepsiburada"}
    price = soup.find('span',{"data-bind":"markupText:'currentPriceBeforePoint'"}).text
    price_after_point = soup.find('span',{"data-bind":"markupText:'currentPriceAfterPoint'"}).text
    price_currency = soup.find('span',{"itemprop":"priceCurrency"}).text
    price = str(f"{price},{price_after_point} {price_currency}")
    try:
        oldPrice = soup.find('del',{'id':'originalPrice'}).text
    except AttributeError:
        oldPrice = None
    imgMain = soup.find('img',{'class':'product-image'})['src']
    title = soup.find('span',{'class':'product-name'}).text
    try:
        rating = soup.find('span',{'class':'rating-star'}).text.strip()
    except AttributeError:
        rating = None
        ratingCount = None
    count=0
    listImages=[]
    while True:
        try:    
            images = soup.find('img',{'id':f"image-{count}"})
            count=count+1
            images=images['data-src']
            listImages.append(images)
        except:
            break
    if rating != None:
        ratingCount = soup.find('a',{'class':'product-comments'}).find('span').text
    else:
        ratingCount=None
    dataDictionary.update({"price": f"{price}",'originalPrice':f'{oldPrice}','main img url': f'{imgMain}','title': f'{title}','rating': f'{rating}','image urls': f'{listImages}','rating count': f'{ratingCount}'})
    liste.append([dataDictionary['website'],price,oldPrice,imgMain,title,rating,dataDictionary['image urls'],ratingCount])
    df = pd.DataFrame(liste)
    df.columns= ["website","price","old price","main img","title","rating","image urls","rating count"]
    with pd.ExcelWriter('hepsiburada.xlsx', mode='w') as writer:
        df.to_excel(writer, sheet_name='Sheet1')
    df.to_csv('hepsiburada.csv')
    with open('hepsiburada.json','w') as fp:
        json.dump(liste, fp)
    print("item added")
        
try:      
    hepsiburada()
except AttributeError:
    print('no attributes found')

email_provider = 'smtp-mail.outlook.com'

server = smtplib.SMTP(email_provider,port= 587)
server.starttls()
server.login(user = sender, password = password)
body = 'Webscraping completed'
msg = f'From: {sender}\r\nTo: {recipient}\r\n\r\n{body}'

server.sendmail(sender, recipient, msg)
server.quit()


