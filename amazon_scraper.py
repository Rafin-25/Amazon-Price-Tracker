from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import datetime

# --- Set up Chrome Options ---
options = Options()
options.add_argument("--headless")

options.add_argument("start-maximized")
# options.add_argument("user-agent=Mozilla/5.0 ...")  # Put real UA here

driver = webdriver.Chrome(options=options)
search_query = "shirt"
url = f"https://www.amazon.com/s?k={search_query}"

driver.get(url)
time.sleep(3)  # Wait for page to load

product_data = []

# Scrape first 5 products
products = driver.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

for product in products:
    try:
        name = product.find_element(By.TAG_NAME, 'h2').text
        price = product.find_element(By.CLASS_NAME, 'a-price-whole').text

        rating_elements = product.find_elements(By.XPATH, './/span[contains(@class,"a-icon-alt")]')
        rating = rating_elements[0].text if rating_elements else "No rating"

        url = product.find_element(By.TAG_NAME, 'a').get_attribute('href')

        product_data.append({
            "Name": name,
            "Price": price,
            "Rating": rating,
            "URL": url
        })
    except Exception as e:
        print("Skipping a product due to missing data:", e)


driver.quit()

# Save to CSV
# Assuming product_data already exists
df = pd.DataFrame(product_data)

# Get current date and time in YYYY-MM-DD_HH-MM-SS format
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Create filename with date and time
filename = f"amazon_products_{timestamp}.csv"

# Save to CSV
df.to_csv(filename, index=False)
print(f"Done. Products saved as {filename}")
