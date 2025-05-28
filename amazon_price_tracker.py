from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.parse
import time
import random
from fake_useragent import UserAgent

def get_driver():
    options = Options()
    options.add_argument('--headless=new')  # Modern headless mode
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    return driver

def price_check(SEARCH: str, PRICE: int) -> list:
    driver = get_driver()

    encoded_search = urllib.parse.quote_plus(SEARCH)
    url = f"https://www.amazon.com/s?k={encoded_search}"

    print(f"[INFO] Fetching URL: {url}")
    driver.get(url)
    time.sleep(random.uniform(3, 5))  # Random delay for stealth

    result = []
    products = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

    for product in products:  # Limit number of products for speed
        try:
            name = product.find_element(By.TAG_NAME, 'h2').text
            try:
                price_whole = product.find_element(By.CSS_SELECTOR, ".a-price-whole").text.replace(',', '')
                price_fraction = product.find_element(By.CSS_SELECTOR, ".a-price-fraction").text
                full_price = float(f"{price_whole}.{price_fraction}")
            except:
                full_price = None
            url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if full_price is not None and full_price <= PRICE:
                result.append({
                    "Name": name,
                    "Price": full_price,
                    "URL": url
                })
        except Exception as e:
            print(f"[ERROR] Skipping product due to error: {e}")
            continue

    driver.quit()
    return result

