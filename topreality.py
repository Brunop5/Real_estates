from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from time import sleep
import pandas as pd


driver = webdriver.Chrome()
driver.implicitly_wait(2)
options = webdriver.ChromeOptions() 


# bot window on
# ---
# Adding argument to disable the AutomationControlled flag
options.add_argument("--disable-blink-features=AutomationControlled") 
 
# Exclude the collection of enable-automation switches
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
# Turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False) 
 
# Setting the driver path and requesting a page 
driver = webdriver.Chrome(options=options) 
 
# Changing the property of the navigator value for webdriver to undefined 
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# ---
# bot window off

actions = ActionChains(driver)

names: list[str] = []
phones: list[list[str]] = []
mails: list[list[str]] = []

first = True
for page in range(1, 400):
    url = f"https://www.topreality.sk/realitne-kancelarie/{page}/"
    try:
        driver.get(url)
    except:
        driver.get(url)

    if first:
        sleep(5)
        first = False

    agencies = driver.find_elements(By.CSS_SELECTOR, value=".listing .card-info")

    for agency in agencies:
        name = agency.find_element(By.CLASS_NAME, value="text-decoration-none.text-dark-gray").text

        numbers = [j.text for j in 
                   agency.find_elements(By.CLASS_NAME, value="click_to_call")]

        mail = [element.text for element in 
                agency.find_elements(By.CSS_SELECTOR, value="a.text-dark-gray.click_to_email")]

    names.append(name)
    phones.append(numbers)
    mails.append(mail)
    print(page)
    print(name, numbers, mail)


data = {"Agency" : names,
        "PhoneNumber" : phones,
        "E-mail" : mails}

df = pd.DataFrame(data)
df.to_csv("Estate_agencies_sk.csv", index=False)
print("DONE")
