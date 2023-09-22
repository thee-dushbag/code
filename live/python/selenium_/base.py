from random import random
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from yarl import URL

HOST, PORT = "localhost", 5052
BASE_URL = URL(f"http://{HOST}:{PORT}")
INDEX_URL = BASE_URL.with_path("")
TEXT_URL = BASE_URL.with_path("/send_text")

options = webdriver.FirefoxOptions()
# options.add_argument('-headless')

driver = webdriver.Firefox(options)
driver.get(str(TEXT_URL))

messages = (
    "My Name is Simon Nganga",
    "I have a Sister",
    "Called Faith Njeri",
    "And My Age is 20",
)


def send_text(driver: webdriver.Firefox, text: str):
    driver.get(str(TEXT_URL))
    form = driver.find_element(By.TAG_NAME, "form")
    text_field = form.find_element(By.ID, "text_field")
    send_text = form.find_element(By.ID, "send_btn")
    for key in text:
        text_field.send_keys(key)
        sleep(random() / 4)
    sleep(0.5)
    send_text.click()
    return driver


for msg in messages:
    send_text(driver, msg)

msgs = driver.find_elements(By.CLASS_NAME, "message")
for msg in msgs:
    print(f"Message Found: {msg.text!r}")

driver.close()
