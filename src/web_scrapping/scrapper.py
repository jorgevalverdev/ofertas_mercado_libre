"""
Mercado Libre Web Scraper

This script scrapes offers from the Mercado Libre website and saves the
data into an Excel file for further analysis.

Dependencies:
- Selenium
- BeautifulSoup
- pandas
"""

import datetime as dt
import os
import pandas as pd
import time
from breakdown import Oferta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Get the current date
time_init = dt.datetime.now()
print(f"Fecha y hora de inicio: {time_init.strftime('%Y-%m-%d %H:%M:%S')}")

# Load the webpage
url = 'https://www.mercadolibre.com.pe/ofertas#nav-header'

# Configure Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--app={url}")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Track the total number of offers
total_ofertas = 0
df_ofertas = Oferta().to_df()

try:
    # Set up WebDriver
    driver_location = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), '../../drivers/chromedriver.exe')
    webdriver_service = Service(os.path.abspath(driver_location))
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    
    # Open the URL
    driver.get(url)

    # Initialize variables
    page_number = 1
    ultima_pagina = False
    
    while not ultima_pagina:
        # Wait for the offers catalog to load
        catalogo_ofertas = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/main/div/section/div[2]/div/div')
            )
        )

        # Parse the catalog HTML
        inner_html = catalogo_ofertas.get_attribute('innerHTML')
        soup = BeautifulSoup(inner_html, 'html.parser')
        child_divs = soup.find_all('div', recursive=False)

        # Extract offers from the catalog
        ofertas_por_pagina = 0
        for div in child_divs:
            df_oferta_row = Oferta(div, page_number)
            if df_oferta_row.precio_oferta is not None:
                df_ofertas = pd.concat(
                    [df_ofertas, df_oferta_row.to_df()], ignore_index=True
                )
                ofertas_por_pagina += 1
        total_ofertas += ofertas_por_pagina

        # Scroll down to load more offers
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Check for the next page button
        ultima_pagina = True
        nav = driver.find_element(By.XPATH, '/html/body/main/div/section/div[2]/nav')
        for li in nav.find_elements(By.TAG_NAME, 'li'):
            if li.get_attribute('class') == \
                    'andes-pagination__button andes-pagination__button--next':
                ultima_pagina = False
                print(f"Página {page_number}: {ofertas_por_pagina} ofertas encontradas")
                page_number += 1
                siguiente = li.find_element(By.TAG_NAME, 'a')
                siguiente.click()
                break
        if ultima_pagina:
            print(f"Página {page_number} (LAST): {ofertas_por_pagina} ofertas encontradas")

except TimeoutException as ex:
    print("Se produjo un error de tiempo de espera: ", ex)

except Exception as ex:
    print(f"Se produjo un error: {ex}")

else:
    # Close the WebDriver and quit the browser
    if driver:
        driver.quit()
        driver = None
        
        # Show this message if the driver was closed as expected
        print("El scrapping ha finalizado correctamente.")
    
    # Show the total number of offers found
    print(f"Cuenta total de ofertas: {total_ofertas}")

    # Save the results to an Excel file
    output_file = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    '../../data/processed/mercado_libre_ofertas.xlsx')
    if os.path.exists(output_file):
        os.remove(output_file)
    df_ofertas.to_excel(output_file, index=False)
    print(f"Archivo Excel creado: {os.path.abspath(output_file)}")

    # Get the end time
    time_end = dt.datetime.now()
    print(f"Fecha y hora de fin: {time_end.strftime('%Y-%m-%d %H:%M:%S')}")

    # Calculate the duration of the scraping
    duration = time_end - time_init
    duration_in_seconds = duration.total_seconds()

    # Print final message with the duration of the scrapping
    print(f"Duración del proceso: {duration_in_seconds:.1f} segundos")

finally:
    # Close the WebDriver and quit the browser
    if driver:
        driver.quit()
        
        # Show this message if the driver was closed unexpectedly
        print("El scrapping ha finalizado debido a una excepción.")
    

