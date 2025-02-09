import pandas as pd
from bs4 import BeautifulSoup

import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


PROXY = "us-mi1-smart.serverlocation.co:3128"

options = Options()
#options.add_argument("--headless")
options.add_argument("--no-sandbox")

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager" # to make the page load faster
# caps["proxy"] = {
#     "httpProxy": PROXY,
#     "ftpProxy": PROXY,
#     "sslProxy": PROXY,
#     "proxyType": "MANUAL",
# }






print('Loading and downloading the driver')
driver = uc.Chrome(desired_capabilities=caps, options=options)
print('Browser loaded')
category='fitness center'
city='New York'
state='New York'

items_list = []
for x in range(1, 270): # you can change the number of pages
    #driver.get(f'https://www.manta.com/search?search_source=nav&search=Doctors&city=Syracuse&state=york&device=desktop&screenResolution=2400x1300&pg={x}')
    #driver.implicitly_wait(30)
    #driver.get(f'https://www.manta.com/search?search_source=nav&search={category}&city={city}&state={state}&device=desktop&screenResolution=2400x1300&pg={x}')
    driver.get(f'https://www.manta.com/search?search={category}&context=unknown&search_source=nav&city={city}&state={state}&country=United%20States&device=desktop&pt=40.6943%2C-73.9249&screenResolution=1584x990&pg={x}')
    print(f'Page {x}')
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mapid"]')))
    soup = BeautifulSoup(driver.page_source, 'lxml')
    cards = soup.select('.md\:mt-4')

    for card in cards:
        try:
            name = card.select_one('.hover\:text-primary-v1').text
        except:
            name = None
        try:
            address_card = card.select('.ml-4 div')
            address = address_card[0].text + ',' + ' ' + address_card[1].text
        except:
            address = None
        try:
            phone = card.select_one('.mt-2 div').text
        except:
            phone = None
        try:
            website = card.select_one('.hover\:underline')['href']
            website = website.replace('/urlverify?redirect=https%3A%2F%2F', '')
            if '/urlverify?redirect' in website:
                website = website.replace('/urlverify?redirect=http%3A%2F%2F', '')
            else:
                pass
            website = website.replace(website[website.index('%'):], '')
        except:
            website = None

        items = {
            'Name': name,
            'Address': address,
            'Phone': phone
            #'Website': website
        }

        items_list.append(items)
    print(items_list)

    df = pd.DataFrame(items_list)
    df.to_csv(f'{category}-{city}-{state}.csv', index=False)

df = pd.DataFrame(items_list)
df.to_csv(f'{category}-{city}-{state}.csv', index=False)
print(df)
driver.quit()