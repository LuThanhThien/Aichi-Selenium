import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from src.globals import URLs
from src.models import Account
from .base_controller import BaseController
from src.utils.html_utils import wait_until_presence

class Access(BaseController):
   def __init__(self, account: Account = None) -> None:
      super().__init__(account)
   
   def login(self, browser: WebDriver):
      try:
         # Max refresh times
         max_refresh = 20
         count_to_login = 0
         while browser.current_url != URLs.login_url:
            if count_to_login == max_refresh:
               # If login is not successful after max refreshing, return
               self.logger.error("Failed to login after {} refreshing".format(max_refresh))
               return
            browser.get(URLs.login_url)
            self.logger.info("Opened login page")
            count_to_login += 1
            time.sleep(1)
            wait_until_presence(browser, By.ID, "userLoginForm.userId")
         

         count_login = 0
         while browser.current_url in [URLs.re_login_url, URLs.login_url]:
            if count_login == max_refresh:
               # If login is not successful after max refreshing, return
               self.logger.error("Failed to login after {} refreshing".format(max_refresh))
               return
            
            # Fill login form
            browser.find_element(By.ID, "userLoginForm.userId").send_keys(self.account.username)
            browser.find_element(By.ID, "userLoginForm.userPasswd").send_keys(self.account.password)
            browser.find_element(By.XPATH, "/html/body/form/main/div/div/div[2]/div/input").click()
            self.logger.info("Logging in")

            # Update count
            count_login += 1
            self.logger.info("Current url: {}".format(browser.current_url))
            time.sleep(0.3)

         self.logger.info("Logged in finished")
         return True
      except Exception as e:
         self.logger.error("Failed to login", e)
         return False


