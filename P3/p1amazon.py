import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import logging

logging.basicConfig(filename='scraper.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

def extract_table_data(product_soup, table_id):
    table = product_soup.find('table', {'id': table_id})
    data_dict = {}
    if table:
        rows = table.find_all('tr')
        for row in rows:
            key_col = row.find('th', class_='a-color-secondary a-size-base prodDetSectionEntry')
            value_col = row.find('td', class_='a-size-base prodDetAttrValue')
            
            if key_col and value_col:
                key = key_col.get_text(strip=True)
                value = value_col.get_text(strip=True)
                data_dict[key] = value
    return data_dict


#______________________________
#______________________________

#swap user agents when called
def get_random_user_agent():
    return random.choice(USER_AGENTS)
USER_AGENTS = [
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


#______________________________
#______________________________



#pre-definitions
products = []
j=1
df = pd.DataFrame(products, columns=['ID', 'Name', 'Price', 'Rating', 'Number of Ratings', 'Product Information'])
data_rows = []



# -- ITERATE SEARCH PAGES --
for i in range(1, 150):

    #my idea is to swap headers between pages, but not between individual products, frequency still might be too much
    headers = {
    'authority': 'www.newegg.com',
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

    url = f"https://www.amazon.com/s?k=laptop&page={i}"
    
    print(f"Processing page {i}")                         
    response = requests.get(url, headers=headers)
    logging.info(f"URL: {url}, Status Code: {response.status_code}")
    if response.status_code != 200:
        logging.error(f"Unexpected status code {response.status_code} for URL: {url}")

        
    soup = BeautifulSoup(response.text, "html.parser")
    product_div = soup.find_all('div', {'data-component-type': 's-search-result'}) 

    #save raw html data (combining the parsing below)
    #with open(f"amazon_html_data_page_{i}.html", "w", encoding='utf-8') as file:
        #file.write(str(soup.prettify()))

   # if not product_div:
    #    with open(f"error_page_{i}.html", "w", encoding="utf-8") as file:
     #       file.write(response.text)
    
    #Extraction of attributes from particular container, appends to the products list.
    for container in product_div:

        name = container.find('span', class_='a-size-medium a-color-base a-text-normal').text if container.find('span', class_='a-size-medium a-color-base a-text-normal') else ''
        price = container.find('span', class_='a-offscreen').text if container.find('span', class_='a-offscreen') else ''
        rating = container.find('span', class_='a-icon-alt').text if container.find('span', class_='a-icon-alt') else ''
        num_ratings = container.find('span', class_='a-size-base').text if container.find('span', class_='a-size-base') else ''

        product_info = container.find('div', class_='s-product-specs-view')
        product_info = product_info.get_text(strip=True, separator='|') if product_info else ''
       

        data_row = {
            'ID': j,
            'Name': name,
            'Price': price,
            'Rating': rating,
            'Number of Ratings': num_ratings,
            'Product Information': product_info
        }

        product_url_container = container.find('a', class_='a-link-normal')

        if product_url_container:
            
            product_url = 'https://www.amazon.com' + product_url_container['href']
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



            #extract table data
            table_data = extract_table_data(product_soup, 'productDetails_techSpec_section_1')
            table_data2 = extract_table_data(product_soup, 'productDetails_techSpec_section_2')
            


            #merge data
            data_row.update(table_data)
            data_row.update(table_data2)
            
        
        #append the row to the DataFrame
        data_rows.append(data_row)
        
        j += 1      
        time.sleep(random.uniform(1,3))
       

    #added to help decrease detection, might do very little based on the small time range but can be adjusted
    time.sleep(random.uniform(4,8))

#scraped data converted into a pandas 'DataFrame' and saved as a csv file
df = pd.DataFrame(data_rows)
df.to_csv('tableAmazonUpdatedFullx.csv', index=False, encoding='utf-8-sig')