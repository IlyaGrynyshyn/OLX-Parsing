from bs4 import BeautifulSoup as BS4
import requests
import time
import csv
import os

url = 'https://www.olx.ua/uk/list/q-pride-rocx/'
HOST = 'https://www.olx.ua/'
name_file = 'Announcement.cs'
headers = {
    'accept' : '*/*',
    "accept-encoding" : "gzip, deflate, br",
    "accept-language" : "en-US,en;q=0.9,ru-UA;q=0.8,ru;q=0.7,uk-UA;q=0.6,uk;q=0.5",
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }

def get_html(url,params=None):
    r = requests.get(url=url,headers=headers,params=params)
    return r

def get_page_count(html):
    soup = BS4(html,'html.parser')
    pagination = soup.find_all("span",class_='item fleft')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1

def get_contend(html):
    soup = BS4(html,"html.parser")
    items = soup.find_all('tr',class_='wrap')
    ad = []
   
    for item in items:
        ad.append({
            'title':  item.find('h3').find('strong').get_text(),
            'link':  item.find('a').get('href').strip(),
            'price':  item.find('p',class_='price').text.strip(),
            'location':  item.find('td',class_="bottom-cell").find('p',class_="lheight16").find('span').text.strip()
        })
    return ad

def save_file(items,path):
    with open(path,'w',newline='') as file:
        writer = csv.writer(file,delimiter='\t', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\r')
        writer.writerow(['Назва','Ссылка','Цена','Город'])
        for item in items:
            writer.writerow([item['title'],item['link'],item['price'],item['location']])


def parse():
    #url = input("Введите URL страницы: ")
    #url = url.strip()
    html = get_html(url=url)
    if html.status_code == 200:
        ad = []
        pages_count = get_page_count(html.text)
        for page in range (1,pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(url,params={"page" : page})
            ad.extend(get_contend(html.text))
            time.sleep(1)
        save_file(ad,name_file)
        print(f'Получено {len(ad)} обьяв')
        os.startfile(name_file)
    else:
        print("Error 404")


parse()

