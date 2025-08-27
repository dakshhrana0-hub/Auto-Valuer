import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

# Expanded brand list
brands = ['maruti suzuki', 'hyundai', 'honda', 'toyota', 'tata', 'mahindra', 'mercedes benz','ford','volkswagen','audi','nissan' ,'bmw', 'kia']
BASE_URL = "https://www.olx.in/cars_c84?filter=make_eq_{}"
car_data = []

def extract_car_info(card):
    title = card.find('div',{'class':'_2Gr10'}).text.strip()
    link = "https://www.olx.in" + card.find('a')['href']
    image = card.find('img')['src']
    location = card.find('div', {'class': '_3VRSm'}).text.strip()
    price = card.find('span', {"class":"_1zgtX"}).text.strip()
    info = card.find('div',{'class':'_21gnE'}).text.strip()
    print(info)
    
    return {
        'Title': title,
        'Link': link,
        'Location': location,
        'Price': price,
        'Information': info,
        'Image':image
    }

for brand in brands:
    print(f"Scraping: {brand}")
    url = BASE_URL.format(brand)
    response = requests.get(url, headers=HEADERS)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = soup.find_all('li', {'class': '_3V_Ww'})
    
    for card in listings:
        
        info = extract_car_info(card)
        info['Brand'] = brand
        if info:
            car_data.append(info)

    time.sleep(2)

df = pd.DataFrame(car_data)
print(df.head())

# Optional: Save to CSV
df.to_csv('../Data/olx_car_listings_expanded.csv', index=False)