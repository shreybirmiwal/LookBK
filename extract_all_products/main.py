from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def nextPage(driver):
    try:
        nextButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "pagination-next-button"))
        )
        isDisabled = nextButton.get_attribute("disabled")
        if isDisabled:
            return False
        else:
            driver.execute_script('arguments[0].click()', nextButton)
            return True
    except Exception as e:
        print("Error navigating to the next page:", e)
        return False


def extractData(driver):
    products = driver.find_elements(By.CLASS_NAME, "catalog-productCard-module__productCard")
    data_list = []

    for product in products:
        try:
            #scroll to product, wait for it to load a littl
            driver.execute_script("arguments[0].scrollIntoView();", product)
            time.sleep(.2)

            name = product.find_element(By.CSS_SELECTOR, 'h2[data-aui="product-card-name"]').text
            price = product.find_element(By.CSS_SELECTOR, 'span.product-price-text.product-price-font-size').text
            image_section = product.find_element(By.CLASS_NAME, "catalog-productCard-module__product-image-section")
            image_url = image_section.find_element(By.TAG_NAME, "img").get_attribute("src")
            
            product_data = {
                "name": name,
                "price": price,
                "image_url": image_url
            }

            print(product_data)
            data_list.append(product_data)
        except Exception as e:
            print("Error extracting data for a product:", e)
    
    return data_list


def main():
    # Load page
    driver = webdriver.Chrome()
    driver.get("https://www.abercrombie.com/shop/us/mens") #use /womens for women
    time.sleep(10)

    all_data = []
    hasPages = True

    #loop through all paginatied pages
    while hasPages:
        all_data.extend(extractData(driver))
        hasPages = nextPage(driver)
        time.sleep(15)


    #save data into a export csv file
    df = pd.DataFrame(all_data)
    df.to_csv('export_products.csv', index=False)

    driver.quit()


if __name__ == "__main__":
    main()