import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import os

import undetected_chromedriver as uc
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

options = Options()
#options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager" # to make the page load faster

def scrape(category, city, state, pageS,pageE):
    st.text('Loading and downloading the driver')
    driver = uc.Chrome(desired_capabilities=caps, options=options)
    st.text('Browser loaded')

    items_list = []
    for x in range(int(pageS), int(pageE)): # you can change the number of pages
        driver.get(f'https://www.manta.com/search?search_source=nav&search={category}&city={city}&state={state}&device=desktop&screenResolution=2400x1300&pg={x}')
        st.text(f'Page {x}')
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
            
            items = {
                'Name': name,
                'Address': address,
                'Phone': phone                
            }

            items_list.append(items)
            
            df0 = pd.DataFrame(items_list)
            df0.to_csv(f"{category}-{city}-{state}-{category}-innerloop0.csv", mode='w', index=False, header=False)
            
        df00 = pd.DataFrame(items_list)    
        df00.to_csv(f"{category}-{city}-{state}-{category}-innerloop.csv", mode='w', index=False, header=False)
        st.dataframe(df00)

    df = pd.DataFrame(items_list)
    st.dataframe(df)
    driver.quit()

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Press to Download",
        csv,
        f"{category}-{city}-{state}-{category}.csv",
        "text/csv",
        key='download-csv'
    )

if __name__ == "__main__":
    st.balloons()
    st.title('🔨 Manta.com Scraper')
    with st.form('Scraper'):
        st.text('If you get any error make sure you choose a valid category, state, city and number of page as well.')
        st.text('So before you click on the scrape button, I will advice you go to the site (https://www.manta.com/business-directory) to test the parameters before inputing them here')
        st.text('Check the page limit as well. Because the site is very sensitive to this parameters.')
        category = st.text_input('Category EX: Restuarants')
        city = st.text_input('City EX: Miami')
        state = st.text_input('State EX: Florida')
        pageS = st.number_input(f'Starting Page number')
        pageE = st.number_input(f'Ending Page number')
        button = st.form_submit_button('scrape')

    if button:
        st.info('Selenium is running, please wait...')
        scrape(category, city, state, pageS,pageE)
        st.text('Successful finished.')

