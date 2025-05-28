from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import urllib.parse
import time
import random
from fake_useragent import UserAgent


def get_driver():
    # proxy = random.choice(PROXIES)
    # print(f"[INFO] Using proxy: {proxy}")
    options = Options()
    # options.add_argument(f'--proxy-server=http://{proxy}')
    options.add_argument('--headless=new')  # Modern headless mode
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.add_argument(f'--user-agent={user_agent}')
    driver = webdriver.Chrome(options=options)

    # Extra stealth settings
    return driver


def price_check(SEARCH: str, PRICE: int) -> list:
    driver = get_driver()
    try:
        encoded_search = urllib.parse.quote_plus(SEARCH)
        url = f"https://www.amazon.com/s?k={encoded_search}"

        print(f"[INFO] Fetching URL: {url}")
        driver.get(url)
        time.sleep(random.uniform(3, 5))  # Random delay for stealth

        result = []
        products = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

        if not products:
            print("[WARNING] No products found. Retrying...")
            driver.quit()
            return price_check(SEARCH, PRICE)

        for product in products:  # Limit number of products for speed
            try:
                name = product.find_element(By.TAG_NAME, 'h2').text

                try:
                    price_whole = product.find_element(By.CSS_SELECTOR, ".a-price-whole").text.replace(',', '')
                    price_fraction = product.find_element(By.CSS_SELECTOR, ".a-price-fraction").text
                    full_price = float(f"{price_whole}.{price_fraction}")
                except:
                    full_price = None

                try:
                    rating = product.find_element(By.CSS_SELECTOR, ".a-icon-alt").text
                except:
                    rating = "No rating"

                url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')

                if full_price is not None and full_price <= PRICE:
                    result.append({
                        "Name": name,
                        "Price": full_price,
                        "Rating": rating,
                        "URL": url
                    })

            except Exception as e:
                print(f"[ERROR] Skipping product due to error: {e}")
                continue

        return result

    finally:
        driver.quit()
