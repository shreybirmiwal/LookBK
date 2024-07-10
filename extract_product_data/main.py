from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

    

def getImageSizes(driver):

    #color name WORKING
    super_color_class = driver.find_element(By.CLASS_NAME, r"shown_in__h3-mfe")
    color_name = super_color_class.find_element(By.CLASS_NAME, "h3__span").text

    # Get images WORKING
    images = driver.find_element(By.CLASS_NAME, r"product-page-images__container")
    image_elements = images.find_elements(By.TAG_NAME, "img")
    image_urls = [image.get_attribute("src") for image in image_elements]
    print(images)
    



    #               primary sizes of the clothes WORKING
    sizes_primary = []
    sizes_primary_elements = driver.find_element(By.CLASS_NAME, r"product-sizes_primary-mfe")
    input_elements = sizes_primary_elements.find_elements(By.TAG_NAME, "input")
    for input_element in input_elements:
        value = input_element.get_attribute("value")

        inStock = True
        parent_element = input_element.find_element(By.XPATH, '..')
        if parent_element.get_attribute('data-state') == 'disabled':
            inStock = False
  
        sizes_primary.append({
            "size": value,
            "inStock": inStock
        })





    # senocndary
    sizes_secondary = []

    try:
        sizes_secondary_elements = driver.find_element(By.CLASS_NAME, r"product-sizes_secondary-mfe")
        input_elements = sizes_secondary_elements.find_elements(By.TAG_NAME, "input")
        for input_element in input_elements:
            value = input_element.get_attribute("value")

            inStock = True
            parent_element = input_element.find_element(By.XPATH, '..')
            if parent_element.get_attribute('data-state') == 'disabled':
                inStock = False
    

            sizes_secondary.append({
                "size": value,
                "inStock": inStock
            })


    except NoSuchElementException:
        print("NO SECONDARY SIZE")
        sizes_secondary = []




    #get price WORKING
    parent_cost_element = driver.find_element(By.CLASS_NAME, r"product-price")
    price = parent_cost_element.find_element(By.CLASS_NAME, r"screen-reader-text").text


    data = {
        "color": color_name,
        "image_urls": image_urls,
        "sizes_primary": sizes_primary,
        "sizes_secondary": sizes_secondary,
        "price" : price
    }
    
    return data


def extractData(driver, link):
    driver.get(link)
    driver.fullscreen_window()

    time.sleep(5)

    name = driver.execute_script("return document.querySelector('.name-and-description-container h1').textContent")

    options_store = []
    try:
        color_swatch = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "swtg-input-outer-wrapper"))
        )        
        color_options = color_swatch.find_elements(By.CLASS_NAME, "swtg-input-inner-wrapper")
            
        for option in color_options:
            try:
                option.click()
                #get all the data for this color option
                options_store.append(getImageSizes(driver))

                time.sleep(2)
            except Exception as e:
                print("Error clicking on a color option:", e)
    except Exception as e:
        print("Error finding color swatch wrapper:", e)


    product_data = {
        "name": name,
        "options": options_store
    }
    return product_data
    


def main():
    driver = webdriver.Chrome()
    driver.fullscreen_window()
    links = ["https://www.abercrombie.com/shop/us/p/emerson-linen-blend-skort-56256822?categoryId=12265&faceout=life&seq=06",
            "https://www.abercrombie.com/shop/us/p/thrift-inspired-fleece-short-54674832?categoryId=6570710&faceout=model&seq=01"
            ]

    extractedData = []

    for link in links:
        out = extractData(driver, link)
        print(out)
        extractedData.append(out)

    
    with open('extracted-data.json', 'w') as file:
        for data in extractedData:
            json.dump(data, file)
            file.write('\n')


if __name__ == "__main__":
    main()