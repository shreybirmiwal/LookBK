## LookBK

2 folders:
1. extract_all_products:
Webscrapes every for-sale item listed on website

2. extract_product_data
Given a link to a specific product, scrape product info and return in JSON

**Demo**
https://youtu.be/wC-qgBTQd10
[![Demo](https://i.imgur.com/nOMUAQY.png)](https://youtu.be/wC-qgBTQd10)




## How to run locally:

extract_all_products:
```bash
  cd extract_all_products
  pip install selenium pandas
  py main.py
```

extract_product_data:
```bash
  cd extract_product_data
  pip install selenium pandas json
  py main.py
```


## Documentation (Extract all products)
Creates a chrome driver:
```py
    driver = webdriver.Chrome()
    driver.get("https://www.abercrombie.com/shop/us/mens") 
```
Goes through all products on page and extracts data
```py
    products = driver.find_elements(By.CLASS_NAME, "catalog-productCard-module__productCard")
    for product in products:
        try:
            #scroll to product, wait for it to load a little
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
```
Checks if the next-page button clickable. If so, clicks
```py
        nextButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "pagination-next-button"))
        )
```
Repeats for all pages, then returns a CSV file!
```py
    #loop through all paginatied pages
    while hasPages:
        all_data.extend(extractData(driver))
        hasPages = nextPage(driver)
        time.sleep(15)


    #save data into a export csv file
    df = pd.DataFrame(all_data)
    df.to_csv('export_products.csv', index=False)
```

## Documentation (Extract product data)
Creates a driver and loops through the provided links
```py
    driver = webdriver.Chrome()
    driver.fullscreen_window()

    extractedData = []

    for link in links:
        out = extractData(driver, link)
        print(out)
        extractedData.append(out)
```
For each link, see if it is real link and extract the item name
```py
    try:
        name = driver.execute_script("return document.querySelector('.name-and-description-container h1').textContent")
    except Exception as e:
        return {"error": "Error retrieving product name"}
```
For each item, click through all the color options
```py
        for option in color_options:
            try:
                option.click()
```
For each color option, extract price, sizing information, etc and return in JSON
```
    data = {
        "color": color_name,
        "image_urls": image_urls,
        "sizes_primary": sizes_primary,
        "sizes_secondary": sizes_secondary,
        "price" : price
    }
```

## Questions
1. **Scaling**:
    - How would you modify the scraper to handle a large number of URLs efficiently?
      First, I would keep a database "cache" of popular items so they do not need to be scraped again. I would also  
    - What techniques would you use to distribute the workload across multiple machines?
2. **Monitoring**:
    - How would you monitor the scraper's performance and ensure it is running smoothly?
    - What tools or services would you use for monitoring?
3. **Debugging**:
    - What strategies would you employ to debug issues with the scraper?
    - How would you handle and log errors encountered during scraping?
4. **Other Considerations**:
    - What other questions or potential issues would you need to explore before implementing a large-scale scraping solution?
    - What are some alternative approaches for extracting data from sites that may be more robust?
