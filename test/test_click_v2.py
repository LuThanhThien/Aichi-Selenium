import sys
sys.path.append(r'C:\Users\USER\Projects\AichiTool\AichiSelenium')
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver

from src.utils.html_utils import wait_until_presence
from src.models import FormInfo, Customer
from src.globals import Accounts, Meta, URLs
from src.controllers.filler import Filler
from src.controllers.access import Access

def click_checkbox(browser: WebDriver, by: str, html: str):
   try:
      checkbox_element = browser.find_element(by, html)
      checkbox_element.click()
   except Exception as e:
      print(e)

if __name__=="__main__":
   account = Accounts.get_test_account(0)
   access = Access(account)
   filler = Filler(account=account)
   
   browser = webdriver.Chrome()
   browser.get(URLs.login_url)
   time.sleep(60)

   access.login(browser)
   
   form_info = FormInfo.default_form()   
   # 30 April 2024
   form_info.url = r"https://www.shinsei.e-aichi.jp/pref-aichi-police-u/offer/offerList_detail?tempSeq=3895&accessFrom=offerList"
   browser.get(form_info.url)
   
   continue_button = browser.find_element(By.XPATH, r'//*[@id="ok"]')
   continue_button.click()
   filler.click_checkbox(browser, By.NAME, "item[6].choiceList[0].checkFlag")
   
   time.sleep(5)
   browser.quit()