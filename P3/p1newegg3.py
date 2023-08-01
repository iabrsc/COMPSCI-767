import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
import logging

logging.basicConfig(filename='newegg.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def extract_table_data(product_soup):
    tables = product_soup.find_all('table', {'class': 'table-horizontal'})
    data_dict = {}
    for table in tables:  
        rows = table.find_all('tr')
        for row in rows:
            key_col = row.find('th')
            value_col = row.find('td')
            
            if key_col and value_col:
                key = key_col.get_text(strip=True)
                value = value_col.get_text(strip=True)
                data_dict[key] = value
    return data_dict

#swap user agents when called
def get_random_user_agent():
    return random.choice(USER_AGENTS)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.5; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/93.0.961.38',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36 Edge/93.0.961.52',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Android 11; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0',
    'Mozilla/5.0 (Android 11; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; SM-G970U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 11.0; Windows NT 10.0; Trident/7.0)',
]

USER_AGENTS_ARCHIVE = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.54',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2)',

]





products = []
df = pd.DataFrame(products, columns=['ID', 'Name', 'Price', 'Rating', 'Number of Ratings'])
#Counter for ID, figured it was easier to start by just generating them myself. Not 100% sure where to find potential ID #'s on the page either...
j=1
data_rows = []

for i in range(16, 30):
    
    #redefine headers between pages (swap user agent)
    headers = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': get_random_user_agent(),
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
    }

    url = f"https://www.newegg.com/p/pl?d=laptop&page={i}"
    print(f"Processing page {i}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    product_containers = soup.find_all('div', {'class': 'item-container'})

   
    for container in product_containers:
        name = ''
        price = ''
        rating = ''
        num_ratings = ''

        if container.find('i', class_='fas fa-info-circle-light') == ' Sponsored':
            continue
        else:
            ''

        product_url_container = container.find('a')
        if product_url_container:
            
            product_url = product_url_container['href']
            print(product_url)

        
            #visit the product page
            product_response = requests.get(product_url, headers=headers)
            
            logging.info(f"Product URL: {product_url}, Status Code: {product_response.status_code}")
            if response.status_code != 200:
                logging.error(f"Unexpected status code {product_response.status_code} for URL: {url}")
            
            product_soup = BeautifulSoup(product_response.text, "html.parser")

            if not product_soup:
                with open(f"error_product_{j}.html", "w", encoding="utf-8") as file:
                    file.write(product_response.text)

            name = product_soup.find('h1', class_='product-title').text if product_soup.find('h1', class_='product-title') else ''
        
            price_li = product_soup.find('li', class_='price-current')
            if price_li:
                main_price_tag = price_li.find('strong')
                if main_price_tag:
                    main_price = main_price_tag.get_text()
                else:
                    main_price = ""
                fractional_price_tag = price_li.find('sup')
                if fractional_price_tag:
                    fractional_price = fractional_price_tag.get_text()
                else:
                    fractional_price = ""
                price = main_price + fractional_price

            #not making it easy for me... 'rating rating-4' as well as 'rating rating-5', but no difference in HTML structure... smh...
            rating_tag = product_soup.find('i', {'class': lambda x: x and x.startswith('rating rating-')})
            if rating_tag and 'title' in rating_tag.attrs:
                rating = rating_tag['title'].split(' ')[0]
            else:
                rating = None

            
            num_ratings_tag = product_soup.find('span', {'title': 'Read reviews...'}, class_='item-rating-num')
            if num_ratings_tag:
                num_ratings = num_ratings_tag.get_text(strip=True).strip('()')
            else:
                num_ratings = None

           
            #create a list essentially, anything found via the function to extract tables should just append to this when i merge them
            data_row = {
            'ID': j,
            'Name': name,
            'Price': price,
            'Rating': rating,
            'Number of Ratings': num_ratings,
            }


            #extract table data
            table_data = extract_table_data(product_soup)
            
            #merge data, I think it screws up when it skips a sponsored item based on my code above, assuming that is working. 
            #EDIT: idk, could be anything, refreshing my terminal makes it work like half the time...
            #EDIT #2: ....yeah... spamming running it until it works, works....
            if data_row:
                data_row.update(table_data)
            else: ''
            
        if data_row:          
            #append the row to the DataFrame
            data_rows.append(data_row)
        else: ''

        j += 1
        time.sleep(random.uniform(1,3))

    time.sleep(random.uniform(3,10))

     

df = pd.DataFrame(data_rows)
df.to_csv('tableNeweggExtraction.csv', index=False)