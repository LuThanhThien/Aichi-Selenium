import os
import time 
import random

from selenium.webdriver.remote.webdriver import WebDriver
from seleniumbase import Driver, SB

from src.logs import Names, BaseLogger
from src.exceptions import BaseException
from src.globals import Meta, Customers
from src.models.customer import Customer

from .access import Access
from .finder import Finder
from .filler import Filler
from src.models import Account


class MainController:
   
   @staticmethod
   def subprocess(index: int, account: Account = None, num_retry: int = 0):
      main_logger = BaseLogger.get(Names.MAIN_CONTROLLER)

      if num_retry > Meta.max_num_retry:
         main_logger.error("Return since max number of retry reached {}".format(Meta.max_num_retry))
         return

      main_logger.info("Subprocess {} started with trial number {}".format(index, num_retry))

      if account is None:
         account = Account.random_account()
         main_logger.error("Account is None, choose a random account: {}".format(account))

      if isinstance(account, dict):
         account = Account(**account)
         main_logger.error("Account is a dictionary, convert to Account object: {}".format(account))
      
      try:
         # Open browser
         browser: WebDriver = Driver(uc=Meta.uc, headless=Meta.headless)
         main_logger.info("Browser opened")
         
         # Initialize controllers
         access = Access(account)
         finder = Finder(account)
         filler = Filler(account)

         # Login
         max_refresh = 20
         count_to_login = 0
         result = False
         while not result:
            if count_to_login == max_refresh:
               # If login is not successful after max refreshing, return
               main_logger.error("Failed to login after {} refreshing".format(max_refresh))
               return 
            result = access.login(browser)
            if result: 
               main_logger.info("Logged in successfully")
               break
            count_to_login += 1
            browser.refresh()
            time.sleep(0.3)
            
         save_path = os.path.join(BaseLogger.child_folder, "screenshot_{}.png".format(account.name))
         browser.save_screenshot(save_path)
         main_logger.info("Screenshot saved to", save_path)

         # Find
         main_logger.info("Finding forms")
         list_form_info = finder.find(browser)
         main_logger.info("Found {} form(s)".format(len(list_form_info)))

         # Fill
         # Shuffle the list of form info
         list_form_info = random.sample(list_form_info, len(list_form_info))
         main_logger.info("Customers: {}".format(Customers.customers))
         while len(list_form_info) > 0:
            # Get customer
            customer = None
            if Customers.num_customers > 0:
               customer_index = index % Customers.num_customers
               customer_info = Customers.get_customer(customer_index)
               customer_info['phone_number'] = Meta.main_phone_number_dash
               customer_info['gender'] = random.choice(['M', 'F'])
               main_logger.info("Customer info index {}: {}".format(customer_index, customer_info))
               customer = Customer.safe_load(**customer_info)
               main_logger.info("Customer index {}: {}".format(customer_index, customer))
            else:
               customer = Customer.random_customer()

            # Get first form info and fill
            form_info = list_form_info.pop(0)
            filler.fill(browser, form_info, customer)

            if form_info.is_filled:
               # If form is filled successfully, remove it from the list
               main_logger.info("Form filled successfully, template sequence: {}".format(form_info.template_seq))
            elif form_info.is_closed:
               # If form is closed, remove it from the list
               main_logger.info("Form is closed, template sequence: {}".format(form_info.template_seq))
            else:
               # If form is filled unsuccessfully, add it back to the list
               main_logger.info("Failed to fill form, template sequence: {}".format(form_info.template_seq))
               list_form_info.append(form_info)

            main_logger.info("Remaining form(s): {}".format(len(list_form_info)))

         main_logger.info("All forms passed")
         time.sleep(3)

      except Exception as e:
         BaseException.raise_exc(e)
         main_logger.exception("Caught exception: " + str(e))
         browser.quit()
         # try to awake the browser
         MainController.subprocess(index, account, num_retry + 1)
      finally:
         main_logger.info("Closing browser")
         browser.quit()
         main_logger.info("Browser closed")



  
