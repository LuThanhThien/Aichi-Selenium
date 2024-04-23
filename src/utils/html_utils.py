import selenium
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def wait_until_presence(browser: WebDriver, by: By, html :str, timeout: int = 10):
    WebDriverWait(browser, timeout).until(EC.presence_of_element_located((by, html)))

def wait_until_clickable(browser: WebDriver, by: By, html: str, timeout: int = 10):
    WebDriverWait(browser, timeout).until(EC.element_to_be_clickable((by, html)))