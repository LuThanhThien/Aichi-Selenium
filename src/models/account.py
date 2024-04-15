import random

from src.globals import Accounts

DEFAULT_USERNAME = "luthien5921@gmail.com"
DEFAULT_PASSWORD = "aichi@5921"

class Account:
   def __init__(self, username, password) -> None:
      assert username, "Username cannot be empty"
      assert password, "Password cannot be empty"

      self.username = username
      self.password = password

   def __str__(self) -> str:
      return f"Username: {self.username}, Password: {self.password}"
   
   @staticmethod
   def test_account():
      return Account(DEFAULT_USERNAME, DEFAULT_PASSWORD)

   @staticmethod
   def random_account():
      random_account = random.choice(Accounts.test_accounts)
      return Account(username = random_account['username'], 
                     password = random_account['password'])

   @staticmethod
   def safe_load(username, password):
      if not username or not password: 
         return Account.test_account
      return Account(username, password)
   
   @property
   def name(self):
      return self.username.split("@")[0]

