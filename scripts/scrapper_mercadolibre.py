from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
import io
# from ..utils.s3.upload_s3 import put_object
from utils.s3.upload_s3 import put_object

AWS_ACCESS_KEY_ID = "AKIARIQLV2TVKLUQTOMF"
AWS_SECRET_ACCESS_KEY = "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"
AWS_BUCKET_NAME = 'mercado-libre-scrapping-prices'
AWS_REGION = 'us-east-1'


def get_browser(headless=True):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    if headless:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    return driver

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

    # Moving to Mercado Livre website
    browser.get("https://www.mercadolivre.com.br/")
    browser.implicitly_wait(5)

    # Moving to "Ofertas" aka "Sale"
    browser.find_element(
        By.XPATH, "/html/body/header/div/div[5]/div/ul/li[2]/a"
    ).click()
    # Get number of pages to iter over each and get data
    number_of_pages = int(
        browser.find_elements(By.CLASS_NAME, "andes-pagination__button")[-2]
        .find_element(By.CLASS_NAME, "andes-pagination__link")
        .text
    ) - 18

    # Accept the cookings
    browser.find_element(
        By.XPATH, "/html/body/div[4]/div[1]/div/div[2]/button[1]"
    ).click()

    data = []

    # Looping over each pages and get all the data inside each product
    for i in range(1, number_of_pages):
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

                # item.find_element(By.CLASS_NAME, "poly-card__content").text

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
                print(ex)
                pass
        # Próxima página
        browser.find_element(
            By.CLASS_NAME, "andes-pagination__button--next"
        ).click()
        browser.implicitly_wait(1)
    return data

def save():
    # Instance of webdriver
    browser = get_browser()
    try:
        data = extract_data_from_website(browser)
        df_data = _transform_in_data_frame(data)
        in_memory_file = _export_to_csv(df_data)
        current_date = datetime.now().strftime('%Y-%m-%d')
        put_object(AWS_BUCKET_NAME, AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY,in_memory_file.getvalue(), f'dados_mercadolivre_{current_date}.csv')

        print('------------- DADO EXTRAÍDO E SALVO NO S3 -------------')
    except Exception as ex:
        print(ex)
    finally:
        browser.quit()

    return data

if __name__ == '__main__':

    save()