import time
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains


from src.globals import URLs, Meta
from src.models import Account, FormInfo, Customer, AccessMessage, EndMessage
from .base_controller import BaseController
from src.utils.html_utils import wait_until_presence

from src.models import FormInfo

class Filler(BaseController):
   def __init__(self, account: Account = None) -> None:
      super().__init__(account)

   def fill(self, browser: WebDriver, form_info: FormInfo, customer: Customer):
      # Access form
      try:
         self.logger.info("Accessing form, template sequence: {}".format(form_info.template_seq))
         self.logger.info("Form URL: {}".format(form_info.url))
         browser.get(form_info.url)
         time.sleep(0.1)
         self.logger.info("Accessed form successfully")
      except Exception as e:
         self.logger.exception("Failed to access form: " + str(e))
         return
      
      # Check if form is available
      max_refresh = 20
      for i in range(max_refresh + 1):
         # Get form message
         form_message = self.get_form_message(browser)
         
         if form_message == AccessMessage.CLOSED:
            # If form is closed, return
            self.logger.info("Form is closed, template sequence: {}".format(form_info.template_seq))
            form_info.set_closed()
            return

         if form_message == AccessMessage.OPENED:
            # Fill form if available
            self.logger.info("Form is available, template sequence: {}".format(form_info.template_seq))
            break
         else:
            if i == max_refresh:
               # If form is not available after max refreshing, return
               self.logger.info("Failed to access form after {} refreshing, template sequence: {}".format(max_refresh, form_info.template_seq))
               return
            # Refresh page if form is still not available
            self.logger.info("Refreshing page to check availability trial number {}, template sequence: {}".format(i+1, form_info.template_seq))
            time.sleep(0.4)
            browser.refresh()

      # Fill form
      self.logger.info("Filling form, template sequence: {}".format(form_info.template_seq))
      try:
         continue_button = browser.find_element(By.XPATH, r'//*[@id="ok"]')
         continue_button.click()
         self.logger.info("Clicked continue button")
      except Exception as e:
         self.logger.exception("Failed to click continue button: " + str(e))
         return

      # Fill inputs
      result_fill = False
      if Meta.keyword == "Tosan" or Meta.keyword == "Hirabari":
         result_fill = self.fill_Tosan_Hirabari(browser, customer)
      else:
         result_fill = self.fill_else(browser, customer)
      # Check if form is filled successfully
      if not result_fill:
         self.logger.error("Failed to fill form, template sequence: {}".format(form_info.template_seq))
         return

      # Check agree and click submit
      try:
         if Meta.onlyday:
            self.click_checkbox(browser, By.NAME, "item[6].choiceList[0].checkFlag")
         else:
            self.click_checkbox(browser, By.XPATH, "/html/body/form/main/div/div[4]/dl[7]/dd/fieldset/p/label/span")
         browser.find_element(By.XPATH, "/html/body/form/main/div/div[5]/div/input").click()
      except Exception as e:
         self.logger.exception("Failed to click submit: " + str(e))
         return
      
      # Check confirm button and click
      try:
         wait_until_presence(browser, By.XPATH, "/html/body/form/main/div/div[3]/div[2]/div/div[2]/button")
         browser.find_element(By.XPATH, "/html/body/form/main/div/div[3]/div[2]/div/div[2]/button").click()
      except Exception as e:
         self.logger.exception("Failed to click confirm button: " + str(e))
         return
      
      # Check if form is filled successfully
      try:  
         # check for success message
         page_src = browser.page_source
         self.logger.info("Get page source successfully")
         if EndMessage.SUCCESS in page_src:
            self.logger.info("Form filled successfully, template sequence: {}".format(form_info.template_seq))
            form_info.set_filled()
         elif EndMessage.FILLED_ALREADY in page_src:
            self.logger.error("Failed to fill form because form has filled already, template sequence: {}".format(form_info.template_seq))
            form_info.set_filled()
         else:
            self.logger.error("Failed to fill form, template sequence: {}".format(form_info.template_seq))
      except Exception as e:
         if EndMessage.DEFENSE_ERROR in str(e):
            self.logger.error("Form filled successfully, template sequence: {}".format(form_info.template_seq))
            form_info.set_filled()
         else:
            self.logger.exception("Failed to check end message: " + str(e))


   def get_form_message(self, browser: WebDriver) -> str:
      try:
         message = browser.find_element(By.XPATH, "/html/body/main/div/form/div[3]/strong/ul/li/span/strong").text   
         self.logger.info("Form message: " + message)
         return message
      except Exception as e:
         self.logger.exception("Failed to get form message, maybe form is available")
         return None
      
   def fill_Tosan_Hirabari(self, browser: WebDriver, customer: Customer):
      try:
         self.fill_input(browser, By.NAME, "item[0].textData2", customer.first_name)
         self.fill_input(browser, By.NAME, "item[0].textData", customer.last_name)
         self.fill_input(browser, By.NAME, "item[1].textData", customer.date_birth)
         self.fill_input(browser, By.NAME, "item[5].textData", customer.phone_number_dash)
         self.select_dropdown(browser, By.NAME, "item[2].selectData", customer.nation)
         self.select_dropdown(browser, By.NAME, "item[3].selectData", customer.country)
         return True
      except Exception as e:
         self.logger.exception("Error occured during fill_Tosan_Hirabari: " + str(e))
         return False
      
   def fill_else(self, browser: WebDriver, customer: Customer):
      try: 
         self.fill_input(browser, By.NAME, "item[0].textData2", customer.first_name)
         self.fill_input(browser, By.NAME, "item[0].textData", customer.last_name)
         self.fill_input(browser, By.NAME, "item[2].textData", customer.date_birth)
         self.fill_input(browser, By.NAME, "item[4].textData", customer.phone_number)
         self.fill_input(browser, By.NAME, "item[5].textData", customer.school_name)
         return True
      except Exception as e:
         self.logger.exception("Error occured during fill_else: " + str(e))
         return False

   def fill_input(self, browser: WebDriver, by: str, html: str, value: str):
      try:
         input_element = browser.find_element(by, html)
         input_element.send_keys(value)
         self.logger.info("Filled input: {} by {}, value: {}".format(html, by, value))
      except Exception as e:
         self.logger.exception("Failed to fill input: " + str(e))

   def choose_radio(self, browser: WebDriver, by: str, html: str):
      try:
         radio_element = browser.find_element(by, html)
         radio_element.click()
         self.logger.info("Chose radio: {} by {}".format(html, by))
      except Exception as e:
         self.logger.exception("Failed to choose radio: " + str(e))

   def click_checkbox(self, browser: WebDriver, by: str, html: str):
      try:
         checkbox_element = browser.find_element(by, html)
         ActionChains(browser).move_to_element(checkbox_element).click(checkbox_element).perform()
         self.logger.info("Check checkbox: {} by {}".format(html, by))
      except Exception as e:
         self.logger.exception("Failed to check checkbox: " + str(e))

   def click_button(self, browser: WebDriver, by: str, html: str):
      try:
         button_element = browser.find_element(by, html)
         ActionChains(browser).move_to_element(button_element).click(button_element).perform()
         self.logger.info("Clicked button: {} by {}".format(html, by))
      except Exception as e:
         self.logger.exception("Failed to click button: " + str(e))


   def select_dropdown(self, browser: WebDriver, by: str, html: str, text: str):
      try:
         dropdown_element = browser.find_element(by, html)
         select = Select(dropdown_element)
         select.select_by_visible_text(text)
         self.logger.info("Selected dropdown: {} by {}, text: {}".format(html, by, text))
      except Exception as e:
         self.logger.exception("Failed to select dropdown: " + str(e))