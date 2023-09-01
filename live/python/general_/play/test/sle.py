from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from yarl import URL
from time import sleep
from random import random

base_url = URL('http://192.168.0.100:5052')
line_site = str(base_url)

options = FirefoxOptions()
# options.add_argument('-headless')

driver = Firefox(options)

lines = [
    'My name is Simon Nganga Njoroge.',
    'I am 20 years old currently.',
    'I love mathematics and programming a little too much.',
    'I want to start a company very soon.',
    'And I want to make a lot of money.'
]

try:
    driver.get(line_site)
    add_line_button = driver.find_element(By.CSS_SELECTOR, '[name="content-add"]')
    send_to_server = driver.find_element(By.ID, 'send-data')
    add_line_input = driver.find_element(By.CSS_SELECTOR, '[name="content-input"]')

    for line in lines:
        for char in line:
            add_line_input.send_keys(char)
            sleep(random() / 4)
        add_line_button.click()

    send_to_server.click()
    sleep(0.8)
except Exception:
    pass
driver.close()