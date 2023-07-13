import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random


#I recognize that the www.amazon.com authority here is incorrect, but I didn't realize it until well into testing, and i don't want to potentially mess up my working code, so I'm leaving it as is
headers = {
    'authority': 'www.newegg.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}


products = []

#Counter for ID, figured it was easier to start by just generating them myself. Not 100% sure where to find potential ID #'s on the page either...
j=0


for i in range(1, 60):
    url = f"https://www.newegg.com/p/pl?d=laptop&page={i}"
    print(f"Processing page {i}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    product_containers = soup.find_all('div', {'class': 'item-container'})

   
    for container in product_containers:
        name_tag = container.find('a', {'class': 'item-title'})
        name = name_tag.text.strip() if name_tag else ''

        price_tag = container.find('li', {'class': 'price-was'})
        price1 = price_tag.text.strip() if price_tag else ''

        price_current_tag = container.find('li', {'class': 'price-current'})
        if price_current_tag:
            dollar_amount_tag = price_current_tag.find('strong')
            cent_amount_tag = price_current_tag.find('sup')

            dollar_amount = dollar_amount_tag.text.strip() if dollar_amount_tag else ''
            cent_amount = cent_amount_tag.text.strip() if cent_amount_tag else ''

            price2 = dollar_amount + cent_amount
        else:
            price2 = ''

        price = price1 if price1 else price2 if price2 else ''



        rating_tag = container.find('i', {'class': 'rating'})
        rating = rating_tag.get('aria-label') if rating_tag else ''

        num_ratings_tag = container.find('span', {'class': 'item-rating-num'})
        if num_ratings_tag:
            num_ratings = num_ratings_tag.text.strip('()')
        else:
            num_ratings = ''

        product_info_tag = container.find('ul', {'class': 'item-features'})
        product_info = product_info_tag.text.strip() if product_info_tag else ''

        products.append([j, name, price, rating, num_ratings, product_info])
        j+=1
    time.sleep(random.uniform(3,10))

     

df = pd.DataFrame(products, columns=['ID', 'Name', 'Price ($)', 'Rating', 'Number of Ratings', 'Product Info'])
df.to_csv('tableNewegg3.csv', index=False)