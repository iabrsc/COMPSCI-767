import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random



#defines HTTP headers; simulates a web browser to make the request appear more... legitimate. 
#Got most of the header information from an request found via 'INSPECT > NETWORK/DEVELOPERTOOLS > request' on the amazon web page. I guessed a bit on some
#   of these, but it seems to work regardless. I'm aware that some of this might be useless/counterintuitive depending on how their page is set up to 
#   prevent scraping
headers = {
    'authority': 'www.amazon.com',
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


#Construct the URL for each page, make a GET request to retrieve HTML content of that particular page. BeautifulSoup parses
#   the HTML for info, looking for particular 'div' elements w/ info. I do not directly know what else happens behind the scenes here, but after
#   numerous trial-and-error it seems to work
for i in range(1, 100):  
    url = f"https://www.amazon.com/s?k=laptop&page={i}"
    print(f"Processing page {i}")                           #helps me check if it is actually running, and maintain my own sanity
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    product_div = soup.find_all('div', {'data-component-type': 's-search-result'}) #this is the WHOLE area of items, not each individual items, perhaps I should narrow it


    #Extraction of attributes from particular container, appends to the products list.
    for container in product_div:

        name = container.find('span', class_='a-size-medium a-color-base a-text-normal').text if container.find('span', class_='a-size-medium a-color-base a-text-normal') else ''
        price = container.find('span', class_='a-offscreen').text if container.find('span', class_='a-offscreen') else ''
        rating = container.find('span', class_='a-icon-alt').text if container.find('span', class_='a-icon-alt') else ''
        num_ratings = container.find('span', class_='a-size-base').text if container.find('span', class_='a-size-base') else ''
        # availability = container.find('span', class_='s-dot').get('aria-label') if container.find('span', class_='s-dot') else '' #soup.find function finds 'span' tag with class 's-dot', then the get method retrieves 'aria-label'

        #conditional info, since it seems not every product has this information, seller info wouldn't pick anything up for some reason

        #seller_info = container.find('span', class_='a-size-base-plus a-color-secondary a-text-normal')
        #seller_info = seller_info.text if seller_info else ''
        product_info = container.find('div', class_='s-product-specs-view')
        product_info = product_info.get_text(strip=True, separator='|') if product_info else ''
        j+=1
        products.append([j, name, price, rating, num_ratings, product_info])

        # -- As a side note, I'm sure it'd be better to separate the specifics out of the "name" attribute (e.g. ram/gpu/all that stuff) but doesn't seem necessary for the goal of this project

    #added to help decrease detection, might do very little based on the small time range but can be adjusted
    time.sleep(random.uniform(3,10)) 

#scraped data converted into a pandas 'DataFrame' and saved as a csv file
df = pd.DataFrame(products, columns=['ID', 'Name', 'Price', 'Rating', 'Number of Ratings', 'Product Information'])
df.to_csv('tableAmazon.csv', index=False)