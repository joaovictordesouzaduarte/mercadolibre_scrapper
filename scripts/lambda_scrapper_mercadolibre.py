import io
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import os
import tempfile
import platform

def get_browser(headless=True):
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/opt/chrome/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-data-dir=/tmp/chrome-user-data")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    try:
        service = Service(executable_path="/opt/chromedriver")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Erro ao iniciar Chrome: {e}")
        raise

def _transform_in_data_frame(data: dict): 
    if data:
        df_data = pd.DataFrame(data=data)
    return df_data

def _export_to_csv(dataframe: pd.DataFrame) -> bytes:
    # Instance of a memory
    io_file = io.BytesIO()
    dataframe.to_csv(io_file, index=False, encoding='latin-1')
    return io_file

def extract_data_from_website(browser):
    try:
        # Moving to Mercado Livre website
        browser.get("https://www.mercadolivre.com.br/ofertas#nav-header")
        browser.implicitly_wait(10)
        print("Acessando Mercado Livre...")
        PAGE_SOURCE = browser.page_source

        # Get number of pages to iter over each and get data

        number_of_pages = int(
            browser.find_elements(By.CLASS_NAME, "andes-pagination__button")[-2]
            .find_element(By.CLASS_NAME, "andes-pagination__link")
            .text
        ) - 18

        # Accept the cookies
        try:
            browser.find_element(
                By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/button[1]"
            ).click()
            print("Cookies aceitos")
        except:
            print("Botão de cookies não encontrado ou já aceito")

        data = []

        # Looping over each pages and get all the data inside each product
        for i in range(1, 2):
            print(f"------------------- Page started: {i} -------------------")
            # Items container
            itens = browser.find_element(
                By.XPATH, "/html/body/main/div/section/div[2]/div"
            ).find_elements(By.CLASS_NAME, "andes-card")

            for item in itens:
                try:
                    #Obtendo todo o conteúdo do produto
                    product_content = item.find_element(By.CLASS_NAME, "poly-card__content")

                    #Obtendo nome
                    product_name = product_content.find_element(By.CLASS_NAME, "poly-component__title").text

                    # Checando se há o elemento span com a classe poly-component__seller
                    seller_name = None
                    try:
                        seller_name = product_content.find_element(By.CLASS_NAME, 'poly-component__seller').text.replace('Por ', '')
                    except NoSuchElementException:
                        print(f'Produto {product_name} não possui nome do vendedor.')
                    
                    product_price_component = product_content.find_element(By.CLASS_NAME, 'poly-component__price')
                    current_price = float(product_price_component.find_element(By.CLASS_NAME, 'poly-price__current').find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text)
                    
                    previous_price = None
                    try:
                        previous_price = float(product_price_component.find_element(By.CLASS_NAME, 'andes-money-amount__fraction').text)
                    except Exception as ex:
                        print(ex)

                    discount = 0 if previous_price is None else current_price / previous_price
                    img = item.find_element(By.CLASS_NAME, 'poly-component__picture').get_attribute('src')

                    data.append(
                        {
                            'date': datetime.now(),
                            'product_name': product_name,
                            'seller': seller_name,
                            'product_price': current_price,
                            'previous_price': previous_price,
                            'discount': discount,
                            'image_url': img
                        }
                    )
                except Exception as ex:
                    print(f"Erro ao processar item: {ex}")
                    continue

        return data
    except Exception as e:
        print(f"Erro durante a extração: {e}")
        return []

def lambda_handler(event, context):
    # Instance of webdriver
    browser = get_browser()
    
    try:
        print('------------- Chrome iniciado com sucesso ----------------')
        # Extract data from website
        data = extract_data_from_website(browser)
        # if data:
        #     # Transform data into dataframe
        #     df = _transform_in_data_frame(data)
            
        #     # Export to CSV
        #     csv_data = _export_to_csv(df)
        #     current_date = datetime.now().strftime('%Y_%m_%d')
            
        #     # Save to file
        #     print('------------- Salvando dados em CSV ----------------')
        #     # Volta uma pasta e salva na pasta data
        #     with open(f'data/mercadolibre_data_{current_date}.csv', 'wb') as f:
        #         f.write(csv_data.getvalue())
            
        #     print(f"Dados salvos com sucesso! {len(data)} produtos extraídos.")
        # else:
        #     print("Nenhum dado foi extraído.")
            
    except Exception as e:
        print('--------------------------------- Erro durante a execução: {e}')
    finally:
        # Close browser
        browser.quit()
        print("Navegador fechado.")