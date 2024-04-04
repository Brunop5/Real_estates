from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import re
import pandas as pd

agencies_urls: list[str] = []
driver = webdriver.Chrome()

for page in range(1, 67):
    url = f'https://realitymix.cz/adresar-realitni-kancelare.php?stranka={page}'
    driver.get(url)

    try:
        driver.find_element(By.CSS_SELECTOR, value = '.CCboxContainer .CCconsBox .content .right button.a').click()
    except:
        pass
    sleep(2)

    urls = driver.find_elements(By.CSS_SELECTOR, value = '.company-list__content h3 a')
    agencies_urls += [i.get_attribute('href') for i in urls]

p_numbers: list[str] = []
names: list[str] = []

for agency_url in agencies_urls:
    driver.get(agency_url)
    sleep(2)
    try:
        try:
            phone_number = driver.find_element(By.CSS_SELECTOR, value = ".ba-info__item-table tr td:last-of-type").text
        except:
            text_with_number = driver.find_element(By.CSS_SELECTOR, value = ".ba-hero__bottom-content-contact strong").text
            phone_number = numbers = re.findall(r'\d+', text_with_number)
    except:
        phone_number = "NOT_FOUND"

    try:
        name = driver.find_element(By.CSS_SELECTOR, value = ".ba-hero__top-content h1 span").text
    except:
        name = "NOT_FOUND"
    if any(existing.lower().startswith(name.lower().split()[0]) for existing in names):
        print(f"Skipping: {name}")
    else:
        names.append(name)
        p_numbers.append(phone_number)


data = {"Agency" : names,
        "PhoneNumber" : p_numbers}

df = pd.DataFrame(data)
df.to_csv('Estate_Agencies_cz', index=False)