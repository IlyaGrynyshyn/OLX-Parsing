from bs4 import BeautifulSoup as BS4
import requests
import csv
import os
import time
host = 'https://auto.ria.com/'
url = 'https://auto.ria.com/uk/newauto/marka-bmw/'
name_file = 'cars.cs'
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Accept" : "*/*"
}


def get_html (url,params=None):
    r = requests.get(url=url,headers=headers,params = params)
    return r

def get_pages_count(html):
    soup = BS4(html, "html.parser")
    pagination = soup.find_all("span",class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1



def get_contend(html):
    soup = BS4(html,"html.parser")
    items = soup.find_all('div', class_='proposition')
    #number_phone = soup.find('a',class_="phone unlink bold load_phone__item proven").find('href')
    #print(number_phone)
    cars = []
    for item in items:
        cars.append({
            'title': item.find('h3', class_='proposition_name').text,
            'link': host + item.find(class_="proposition_link").get('href'),
            "price_in_USD": item.find(class_='proposition_price').find(class_='green bold size18'),
            "price_in_UAH": item.find(class_='proposition_price').find(class_='grey size13'),
            'location': item.find(class_='proposition_region size13').find_next('strong')
        })
        print(cars)




def save_file(items,path):
    with open(path,'w', newline='') as file:
        writer = csv.writer(file,delimiter = ';')
        writer.writerow(["Марка","Ссылка","Цена в дол","Цена в грн","Город"])
        for item in items:
            writer.writerow([item["title"], item["link"], item["price_in_USD"], item["price_in_UAH"], item["location"]])
            print(item)


def parse():
    #url = input("Enter URL: ")
    #url = url.strip()
    html = get_html(url=url)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range (1,pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(url,params={"page" : page})
            cars.extend(get_contend(html.text))
            time.sleep(3)
        save_file(cars,name_file)
        print(f'Получено {len(cars)} автомобилей')
        os.startfile(name_file)
    else:
        print("Error 404")

parse()