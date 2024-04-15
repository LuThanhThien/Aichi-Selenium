
from src.models import Account
from src.logs import BaseLogger

class BaseController:
   def __init__(self, account: Account = None) -> None:
      if isinstance(account, dict):
         self.account = Account(**account)
      else:
         self.account = account
      self.logger = BaseLogger.get(self.account.name)