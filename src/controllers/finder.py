from typing import List
import time

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

from src.globals import URLs, Meta
from .base_controller import BaseController
from src.models import Account, FormInfo


class Finder(BaseController):
   def __init__(self, account: Account = None) -> None:
      super().__init__(account)
      self.list_form_info: List[FormInfo] = []
      self._max_forms = 10

   def find(self, browser: WebDriver) -> List[FormInfo]:
      if browser.current_url != URLs.main_url:
         browser.get(URLs.main_url)
      self.logger.info("On main page")
      self._search(browser)
      self._collect(browser)

      start_time = time.time()
      while len(self.list_form_info) == 0:
         self.logger.error("No form found")
         # Refresh and try again
         time.sleep(1)
         browser.refresh()
         self._collect(browser)

         if time.time() - start_time > Meta.timeout:
            self.logger.error("Timeout {}s > {}s".format(time.time() - start_time, Meta.timeout))
            break
         
      return self.list_form_info

   def _search(self, browser: WebDriver) -> None:
      browser.find_element(By.ID, "offerListForm.templateName").send_keys(Meta.keyword)
      browser.find_element(By.XPATH, "/html/body/form/main/div/div[4]/div[1]/div[2]/div/input").click()
      self.logger.info("Search submitted")

   def _collect(self, browser: WebDriver) -> None:
      # Collect forms
      form_table = browser.find_element(By.XPATH, "/html/body/form/main/div/div[5]/div/ul")
      forms = form_table.find_elements(By.TAG_NAME, "li")
      self.logger.info("Collected {} forms".format(len(forms)))

      # Collect form info from text
      self.list_form_info = []
      for form in forms:
         hidden_input = form.find_element(By.XPATH, ".//div[@style='display:none']/input")
         temp_seq = hidden_input.get_attribute("value")
         form_text = form.text + "\n" + temp_seq
         form_info = self._parse_data(form_text)

         # Skip if form is passed, ended, or not today ==> Filtered
         if any([form_info.is_passed_status and not Meta.test_mode, 
                 form_info.is_not_today and not Meta.test_mode,
                 form_info.is_ended_status,]):
            # self.logger.info("Skip form with passed, ended, or not today status")
            continue
         
         if Meta.onlyday and form_info.title.__contains__("＜"):
            # self.logger.info("Skip form with ＜ in title for onlyday mode")
            continue

         # Append form info to list
         self.list_form_info.append(form_info)
         if len(self.list_form_info) >= self._max_forms:
            break
      
      self.list_form_info = sorted(self.list_form_info, key=lambda x: x.datetime_diff)

      self.logger.info("Number of filtered forms left is: {} form(s)".format(len(self.list_form_info)))
      for form_info in self.list_form_info:
         self.logger.info("{}".format(form_info))

   def _parse_data(self, form_info_text: str) -> FormInfo:
      # self.logger.info(form_info_text)
      text_list = form_info_text.split("\n")
      title = text_list[0]
      status = text_list[1] if len(text_list) >= 8 else None
      start_date_str = text_list[-6] + " " + text_list[-5]
      end_date_str = text_list[-3] + " " + text_list[-2]
      template_seq = text_list[-1]
      # self.logger.info("Parsed data: title: {}, status: {}, start_date: {}, end_date: {}, template_seq: {}".format(title, status, start_date_str, end_date_str, template_seq))
      form_info = FormInfo(title, status, start_date_str, end_date_str, template_seq)
      return form_info
   