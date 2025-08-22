import io
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import tempfile
import boto3
from botocore.exceptions import ClientError
import logging

def get_browser():
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = "/opt/chrome/chrome"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(f"--user-data-dir={tempfile.mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("user-agent=Mozilla/5.0 ...")
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


def upload_file_to_s3(buffer, bucket_name, object_name=None):
    """Upload a file to an S3 bucket.

    :param file_path: Path to the local file to upload.
    :param bucket_name: Name of the S3 bucket.
    :param object_name: S3 object name. If not specified, the base name of file_path is used.
    :return: True if file was uploaded, else False.
    """
    s3_client = boto3.client('s3', aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
    try:
        s3_client.put_object(Bucket=bucket_name, Key=object_name, Body=buffer.getvalue())
        logging.info(f"File '{buffer}' uploaded to '{bucket_name}/{object_name}'")
        return True
    except ClientError as e:
        logging.error(e)
         
        return False
def _transform_in_data_frame(data: dict): 
    if data:
        df_data = pd.DataFrame(data=data)
    return df_data

def _export_to_csv(dataframe: pd.DataFrame) -> bytes:
    # Instance of a memory
    csv_buffer = io.StringIO()
    dataframe.to_csv(csv_buffer, index=False, encoding='latin-1')
    return csv_buffer

def extract_data_from_website(browser):
    try:
        # Moving to Mercado Livre website
        browser.get("https://www.mercadolivre.com.br/ofertas#nav-header")
        print("Acessando Mercado Livre...")
        PAGE_SOURCE = browser.page_source

        wait = WebDriverWait(browser, 12)
        # Desabilita implicit waits para evitar atrasos em elementos opcionais
        browser.implicitly_wait(0)

        # Accept the cookies
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/button[1]"))).click()
            print("Cookies aceitos")
        except:
            print("Botão de cookies não encontrado ou já aceito")

        # Wait for items to be present on the page
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "andes-card")))

        # Get number of pages to iter over each and get data (if needed later)
        try:
            # Get only the first five pages
            pages = browser.find_elements(By.CLASS_NAME, "andes-pagination__button")[:5]
        except Exception as ex:
            raise Exception("Não foi possível obter o número de páginas")

        # Looping over each pages and get all the data inside each product
        data = []
        for i, page in enumerate(pages):

            if i == 0:
                continue
            print(f"------------------- Page started: {i} -------------------")
            browser.get(f"https://www.mercadolivre.com.br/ofertas?page={i}")
            # Items container
            itens_container = browser.find_element(By.XPATH, "/html/body/main/div/section/div[2]/div")
            itens = itens_container.find_elements(By.CLASS_NAME, "andes-card")
            for item in itens:
                try:
                    #Obtendo todo o conteúdo do produto
                    product_content = item.find_element(By.CLASS_NAME, "poly-card__content")

                    #Obtendo nome
                    product_name = product_content.find_element(By.CLASS_NAME, "poly-component__title").text

                    # Checando se há o elemento span com a classe poly-component__seller via JS (mais rápido e sem esperas)
                    seller_name = browser.execute_script(
                        "const el = arguments[0].querySelector('.poly-component__seller'); return el ? el.innerText.replace(/^Por\\s+/, '') : null;",
                        product_content
                    )
                    
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
# def lambda_handler():
    print("Iniciando scrapper...")
    # Instance of webdriver
    browser = get_browser()
    
    try:
        print('------------- Chrome iniciado com sucesso ----------------')
        # Extract data from website
        data = extract_data_from_website(browser)
        if data:
            # Transform data into dataframe
            df = _transform_in_data_frame(data)
            # Export to CSV
            buffer = _export_to_csv(df)
            current_date = datetime.now().strftime('%Y_%m_%d')
            
            # Save to file
            print('------------- Salvando dados em CSV ----------------')            
            # Salva no S3
            upload_file_to_s3(buffer, 'mercadolibre-scrapper-data', f'mercadolibre_data_{current_date}.csv')
            print(f"Dados salvos com sucesso! {len(data)} produtos extraídos.")
        else:
            print("Nenhum dado foi extraído.")
            
    except Exception as e:
        print('--------------------------------- Erro durante a execução: {e}')
    finally:
        # Close browser
        browser.quit()
        print("Navegador fechado.")

if __name__ == '__main__':
    lambda_handler()