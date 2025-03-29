import os
# import sys
import time
from breakdown import Oferta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import pandas as pd

# Load the webpage
url = 'https://www.mercadolibre.com.pe/ofertas#nav-header'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--app={url}") 
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("start-maximized")
# chrome_options.add_argument("--window-size=720,480")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

webdriver_service = Service("../../drivers/chromedriver.exe") #Your chromedriver path
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

try:
    # Open the URL
    driver.get(url)  # Replace with the URL of the webpage you want to scrape
    
    # Initial values
    page_number = 1 # This variable is used to keep track of the page number
    df_ofertas = Oferta().to_df() # Initialize an empty DataFrame to store the offers
    ultima_pagina = False # This variable is used to check if the last page has been reached
    total_ofertas = 0 # This variable is used to keep track of the total number of offers found
    
    while not ultima_pagina:
    
        # Locate the div element containing the offers
        # Use WebDriverWait to wait for the div with catalog info to be clickable
        catalogo_ofertas = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/main/div/section/div[2]/div/div'))
        )
        
        # Get the div elements inside the div element containing the offers
        inner_html = catalogo_ofertas.get_attribute('innerHTML')
        soup = BeautifulSoup(inner_html, 'html.parser')
        child_divs = soup.find_all('div', recursive=False)
        
        # Loop through each child div and extract the information
        # Accumulate the data into a DataFrame
        ofertas_por_pagina = 0
        for div in child_divs:
            df_oferta_row = Oferta(div, page_number)
            if df_oferta_row.precio_oferta is not None:
                df_ofertas = pd.concat([df_ofertas, df_oferta_row.to_df()], ignore_index=True)
                ofertas_por_pagina += 1
        total_ofertas += ofertas_por_pagina
        
        # Scroll down to load more offers
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Check if there is a next page button and click it
        ultima_pagina = True
        nav = driver.find_element(By.XPATH, '/html/body/main/div/section/div[2]/nav')
        for li in nav.find_elements(By.TAG_NAME, 'li'):
            # Check if the element is the next page button
            if li.get_attribute('class') == 'andes-pagination__button andes-pagination__button--next':
                ultima_pagina = False
                print(f"Página {page_number}: {ofertas_por_pagina} ofertas encontradas")
                page_number += 1
                # Click the next button
                siguiente = li.find_element(By.TAG_NAME, 'a')
                siguiente.click()
                break
        if ultima_pagina:
            print(f"Página {page_number} (LAST): {ofertas_por_pagina} ofertas encontradas")        
    
except TimeoutException as ex:
    print("Se produjo un error de tiempo de espera: ", ex)

except Exception as ex:
    print(f"Se produjo un error: {ex}")

finally:
    # Print the total number of offers found
    print(f"Cuenta total de ofertas del scrapping: {total_ofertas}")
    # Save the DataFrame to an Excel file
    output_file = os.getcwd() + '/../../data/processed/mercado_libre_ofertas.xlsx'.replace('/', '\\')
    if os.path.exists(output_file):
        os.remove(output_file)
    df_ofertas.to_excel(output_file, index=False)
    print(f"Archivo Excel creado: {os.path.abspath(output_file)}")
    if driver:
        # Close the WebDriver
        driver.quit()

