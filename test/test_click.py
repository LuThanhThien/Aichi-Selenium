import sys
sys.path.append(r'C:\Users\USER\Projects\AichiTool\AichiSelenium')
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium import webdriver

from src.utils.html_utils import wait_until_presence
from src.models import FormInfo, Customer
from src.globals import Accounts
from src.controllers.filler import Filler

def click_checkbox(browser: WebDriver, by: str, html: str):
   try:
      checkbox_element = browser.find_element(by, html)
      checkbox_element.click()
   except Exception as e:
      print(e)

if __name__=="__main__":
   account = Accounts.get_test_account(0)
   filler = Filler(account=account)
   
   browser = webdriver.Chrome()
   form_info = FormInfo.default_form()   
   form_info.url = r"c:\Users\USER\Projects\AichiTool\hhh.html"
   customer = Customer.random_customer()

   wait_until_presence(browser, By.NAME, "item[6].choiceList[0].checkFlag")
   filler.fill_Tosan_Hirabari(browser, customer)
   # filler.click_checkbox(browser, By.NAME, "item[6].choiceList[0].checkFlag")
   filler.click_checkbox(browser, By.XPATH, "/html/body/form/main/div/div[4]/dl[7]/dd/fieldset/p/label/span"
   )
   
   time.sleep(5)
   browser.quit()