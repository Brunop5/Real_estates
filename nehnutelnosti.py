from selenium import webdriver
from selenium.webdriver.common.by import By
from multiprocessing import Pool
import re
import pandas as pd

from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.by import By

def do(page):
    print(page)
    # It's generally a good idea to configure Selenium to run headless in such scripts
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    
    driver = webdriver.Chrome()
    driver.implicitly_wait(2)
    url = f"https://www.nehnutelnosti.sk/bratislava/?p[page]={page}"
    try:
        driver.get(url)
    except Exception as e:
        print(f"Error accessing page {page}: {e}")
        return []
    
    prices = [i.text for i in driver.find_elements(By.CSS_SELECTOR, value='.advertisement-item--content__price-unit')]
    driver.quit()
    return prices

pages = range(1, 405)
all_prices = []
with Pool(processes=8) as pool:  # using None defaults to os.cpu_count()
    results = pool.map(do, pages)
    # Flatten the list of lists
    prices = [price for sublist in results for price in sublist]



out = pd.DataFrame({'Price' : prices})
out.to_csv('Bratislava.csv')
print("Done")

df = pd.read_csv('Bratislava.csv')

monthly = []
total = []

for price in df['Price']:
    if type(price) != str:
        continue
    price = price.replace(',', '.')
    price_float = float(re.findall('(\d{1,3}(?:\s?\d{3})*(?:\.\d+)?)', price)[0].replace(' ', ''))
    if price.endswith('.'):
        if price_float < 1000:
            monthly.append(price_float)
    else:
        total.append(price_float)

print(max(monthly))
print(max(total))
