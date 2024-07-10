# LookBK

Web scraped Abercrombie website and returns in JSON format

2 folders:
1. extract_all_products:
Webscrapes every for-sale item listed on website

2. extract_product_data
Given a link to a specific product, scrape product info and return in JSON## Run Locally

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