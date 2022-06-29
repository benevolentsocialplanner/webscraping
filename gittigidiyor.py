import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import smtplib

liste=[]
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.115 Safari/537.36"}
recipient = input("enter your mail addr to recieve the email")
senderMail = input("enter the sender mail addr")
senderPassword = input("enter the sender password")
def proxy(proxy,url):    
    
    try:
        r = requests.get(url,headers=headers,proxies={'http': proxy,'https':proxy},timeout=3)
        print("successful connection")
    except:
        r = requests.get(url,headers=headers)
        print("you are using your own proxy")
    return r

def proxy(url):
    r = requests.get(url,headers=headers)
    return r

def gittigidiyor():
    url = input("enter the urls seperated by comma: ")
    urlList = url.split(",")
    for url in urlList:
        soup = BeautifulSoup(proxy(url).content,features="lxml") ###### change the proxy parameters if you want to change your proxy in line 28 and 35
        category = soup.find('section',{"class":"products"})
        if category!=None:
            itemsfull = soup.find('section',{"class":"products"})
            items = itemsfull.find_all('li',{"class":"list-item"})
            for item in items:
                url=item.a.get("href")
                soup = BeautifulSoup(proxy(url).content,features="lxml") ###### change the proxy parameters if you want to change your proxy in line 28 and 35
                try: #checking if the item is closed
                    price = soup.find('span',{"id":"sp-price-highPrice"}).text.strip()
                except:
                    continue
                process(url,soup)
        else:
            process(url,soup)
        print("all items of this element are added")

def process(url,soup):
    title = soup.find('h1',{"class":"title r-onepp-title"}).text
    price = soup.find('span',{"id":"sp-price-highPrice"}).text.strip()
    try:
        reviewCount = soup.find('li',{"id":"sp-totalTransaction-container"})
        reviewCount = reviewCount.find('span',{"id":"sp-totalTransaction"}).text
    except AttributeError:
        reviewCount=0
    try:
        review = soup.find('li',{"id":"sp-positiveCommentPercentage-container"})
        review=review.find('span',{"id":"sp-positiveCommentPercentage"}).text
    except AttributeError:
        review=0
    mainImage = soup.find('li',{"class":"img_slide swapimg"}).find('img')['src']
    images=soup.find_all('li',{"class":"img_slide swapimg"})
    listImages=[]
    for image in images:
        image = image.find('img')['data-original']
        listImages.append(image)
    dataDictionary = ({'website':'gittigidiyor',"main img": f"{mainImage}","other images":f"{listImages}","title":f"{title}","price":f"{price}","reviewCount":f"{reviewCount}","review":f"{review}"})
    liste.append([dataDictionary['website'],mainImage,dataDictionary["other images"],title,price,reviewCount,review])
    print("item added")
    df = pd.DataFrame(liste)
    df.columns= ["website","main img","other images","title","price","review count","rating"]
    with pd.ExcelWriter('gittigidiyor.xlsx', mode='w') as writer:
        df.to_excel(writer, sheet_name='Sheet1')
    df.to_csv('gittigidiyor.csv')
    with open('gittigidiyor.json','w') as fp:
        json.dump(liste, fp)


try:       
    gittigidiyor()
except AttributeError:
    print('no attributes found')
    
email_provider = 'smtp-mail.outlook.com'

sender = senderMail
server = smtplib.SMTP(email_provider,port= 587)
server.starttls()
server.login(user = sender, password = senderPassword)
body = 'Webscraping completed'
msg = f'From: {sender}\r\nTo: {recipient}\r\n\r\n{body}'

server.sendmail(sender, recipient, msg)
server.quit()
print("mail sent")
