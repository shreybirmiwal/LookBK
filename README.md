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

**Scaling**:
```
1. How would you modify the scraper to handle a large number of URLs efficiently?
First, I would keep a database "cache" of popular items so they do not need to be scraped again. I would also process them in parallel whilst keeping a list of successes, failures, and resulted scraped data.

2. What techniques would you use to distribute the workload across multiple machines?
A centralized list of tasks (items to scrape) can be kept and delegated through different cloud functions. A central server can store the results of the datascrape.
```
**Monitoring**:
```
1. How would you monitor the scraper's performance and ensure it is running smoothly?
The central database will store all the past scraped data. It can also store which ones had errors and what the error was. From this, a list of stats can be generated with a simple script such as performance, hit rate, cache hit rate, etc

2. What tools or services would you use for monitoring?
I would (through script) save all the links that led to an error in a separate CSV. Then, I would use the perplexity api or some other website scraper api in order to sort the issue. The script would compare for example a screenshot of the website and the returned output. EI: [404 page] compared with {error: item_out_of_stock} will be flagged for manual review since the errors don't match up.
```
**Debugging**:
```
1.What strategies would you employ to debug issues with the scraper?
First, a manual review to see why the item was 'special' or different to cause the error. Then, examine what part of code excludes said edge case.

2.How would you handle and log errors encountered during scraping?
Currently, in the code you can see many 'try catch' blocks which help make sure if an error occurs the script can still proceed. This is key because if it was processing 1,000,000 items, and on the last few items failed, then all of your data could go to waste without the try-catch block. In addition, you can also see in the code checks to see if the product is not a broken link.
```
**Other Considerations**:
```
1. What other questions or potential issues would you need to explore before implementing a large-scale scraping solution?    
Rate limiting and IP blockching are the primary issues. To solve these, I think using rotating proxys could work. In addition, could try different web drivers with different headers (not just selenium)

2. What are some alternative approaches for extracting data from sites that may be more robust?
Can try some API's like this: https://rapidapi.com/axesso/api/axesso-walmart-data-service/playground/apiendpoint_15d12e8f-bbdf-473a-bed3-41c637b78feb (walmart API), or the Amazon API (which has products from Nike, etc). Can also try to partner with a few stores to get more data.
```
