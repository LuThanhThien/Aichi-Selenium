import re
import random

from src.utils import data_utils as du
from src.utils import file_utils as fu
from src.globals import Fake

class Customer:
   def __init__(self,
                last_name: str,
                first_name: str,
                gender: str,
                date_birth: str,
                phone_number: str,
                nation: str,
                country: str,
                school_name: str = None,
                prefacture: str = None,
                examin_number: str = None,
                ) -> None:
      assert last_name, "Last name cannot be empty"
      assert first_name, "First name cannot be empty"
      assert gender in ["F", "M"], "Gender must be either 'F' or 'M'"
      assert date_birth, "Date of birth cannot be empty"
      assert phone_number, "Phone number cannot be empty"
      assert nation, "Nation cannot be empty"
      assert country, "Country cannot be empty"

      self.last_name = last_name 
      self.first_name = first_name
      self.gender = gender
      self.date_birth = du.only_numbers(date_birth)
      self.phone_number = du.undash_format(phone_number)
      self.phone_number_dash = du.dash_format(phone_number)
      self.nation = nation
      self.country = country

      # Hirabari specific
      self.school_name = school_name if school_name else random.choice(Fake.school_name)
      self.prefacture = prefacture if prefacture else random.choice(Fake.prefacture)
      self.examin_number = examin_number if examin_number else random.choice(Fake.examin_number)

      # Forms filled
      self.forms = []

      # Flags
      self._busy = False
      self._filled = False

   def update(self):
      pass

   def fill(self):
      self._filled = True

   def unfill(self):
      self._filled = False
   
   def set_busy(self):
      self._busy = True

   def set_free(self):
      self._busy = False

   @property
   def is_filled(self):
      return self._filled
   
   @property
   def is_busy(self):
      return self._busy

   @staticmethod
   def random_customer():
      nation = random.choice(Fake.nation)
      return Customer(
         last_name=random.choice(Fake.last_name),
         first_name=random.choice(Fake.first_name),
         date_birth=random.choice(Fake.date_birth),
         gender=random.choice(Fake.gender),
         phone_number=random.choice(Fake.phone_number),
         nation=nation,
         country=nation,
         school_name=random.choice(Fake.school_name),
         prefacture=random.choice(Fake.prefacture),
         examin_number=random.choice(Fake.examin_number)
      )
   
   @staticmethod
   def safe_load(last_name: str,
                first_name: str,
                gender: str,
                date_birth: str,
                phone_number: str,
                nation: str,
                country: str,
                school_name: str = None,
                prefacture: str = None,
                examin_number: str = None) -> 'Customer':
      if not last_name: last_name = random.choice(Fake.last_name)
      if not first_name: first_name = random.choice(Fake.first_name)
      if gender: gender = gender.capitalize()
      if gender not in ["F", "M"]: gender = random.choice(Fake.gender)
      if not date_birth: date_birth = random.choice(Fake.date_birth)
      if len(du.only_numbers(date_birth)) > 8: date_birth = du.only_numbers(date_birth)[:8]
      if len(du.only_numbers(date_birth)) < 8: date_birth = du.only_numbers(date_birth) + "1"*(8-len(du.only_numbers(date_birth)))
      if not phone_number: phone_number = random.choice(Fake.phone_number)
      if len(du.only_numbers(phone_number)) > 11: phone_number = du.only_numbers(phone_number)[:11]
      if len(du.only_numbers(phone_number)) < 11: phone_number = du.only_numbers(phone_number) + "0"*(11-len(du.only_numbers(phone_number)))
      if not nation: nation = random.choice(Fake.nation)
      if not country: country = random.choice(Fake.country)

      return Customer(
         last_name=last_name,
         first_name=first_name,
         gender=gender,
         date_birth=date_birth,
         phone_number=phone_number,
         nation=nation,
         country=country,
         school_name=school_name,
         prefacture=prefacture,
         examin_number=examin_number
      )
      

   def __str__(self) -> str:
      return f"{self.last_name} {self.first_name}, {self.gender}, {self.date_birth}, {self.phone_number_dash}, {self.nation} {self.country}"

if __name__=="__main__":
   customer1 = Customer.random_customer()
   tosan_customer1 = Customer("Thien", "Hoang", "M", "1990-01-01",  "090-1234-5678", "日本", "日本")
   tosan_customer2 = Customer.safe_load("", "Hoang", "m", None,  "090-1234-56", "日本", "日本")
   print(customer1)
   print(tosan_customer1)
   print(tosan_customer2)