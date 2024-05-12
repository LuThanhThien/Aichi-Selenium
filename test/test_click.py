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
   browser = webdriver.Chrome()

   account = Accounts.get_test_account(0)
   customer = Customer.random_customer()
   print("Test account: ", account)

   form_info = FormInfo.default_form()   
   # form_info.url = r"c:\Users\USER\Projects\AichiTool\hhh.html"
   form_info.url = r"C:\Users\USER\Projects\AichiTool\AichiSelenium\logs\2024_05_06\05_26_14\form_benemmai380.html"
   
   
   browser.get(form_info.url)
   

   options = [
      {
         "keyword": "Hirabari",
         "type": "checkbox",
         "by": By.XPATH,
         "html": "/html/body/form/main/div/div[4]/dl[7]/dd/fieldset/p/label/span"
      },
      {
         "keyword": "Hirabari",
         "type": "checkbox",
         "by": By.NAME,
         "html": "item[6].choiceList[0].checkFlag"
      },
      {
         "keyword": "Tosan",
         "type": "checkbox",
         "by": By.NAME,
         "html": "item[7].choiceList[0].checkFlag"
      },
      {
         "keyword": "Tosan",
         "type": "button",
         "by": By.XPATH,
         "html": "/html/body/form/main/div/div[5]/div/input"
      }
   ]

   choose_checkbox = 2
   choose_button = 3
   wait_until_presence(browser, options[choose_checkbox]["by"], options[choose_checkbox]["html"])
   filler = Filler(account=account)
   filler.fill_Tosan_Hirabari(browser, customer)
   filler.click_checkbox(browser, options[choose_checkbox]["by"], options[choose_checkbox]["html"])
   filler.click_button(browser, options[choose_button]["by"], options[choose_button]["html"])
   time.sleep(5)
   browser.quit()