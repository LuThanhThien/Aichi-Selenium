
from selenium.webdriver.remote.webdriver import WebDriver
from seleniumbase import Driver

from src.globals import URLs

class BrowserContainer:
   def __init__(self, 
                driver: WebDriver = None
                ):
      self.driver: WebDriver = driver
      self.history_urls = []
      self._open = False
   
   def open(self, url: str):
      self.driver.get(url)
      self._open = True
      self.history_urls.append(url)

   def close(self):
      self.driver.quit()
      self._open = False
      return self

   def reload(self):
      self.driver.refresh()
      return self

   def save_html(self, filename: str):
      with open(filename, 'w') as file:
         file.write(self.driver.page_source)

   def screenshot(self, filename: str):
      self.driver.save_screenshot(filename)

   def navigate_back(self):
      self.driver.back()
      return self
   
   def navigate_forward(self):
      self.driver.forward()
      return self

   def navigate_main_page(self, driver: WebDriver):
      driver.get(URLs.main_url)
   
   @property
   def current_url(self):
      return self.driver.current_url
   
   @property
   def title(self):
      return self.driver.title

   @staticmethod
   def new(**kwargs) -> 'BrowserContainer':
      driver: WebDriver = Driver(**kwargs)
      return BrowserContainer(driver)
