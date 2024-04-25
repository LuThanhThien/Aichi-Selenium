import re 
from datetime import datetime
from pytz import timezone

JAPAN_TIMEZONE = timezone('Asia/Tokyo')
DATETIME_FORMAT = r'%Y-%m-%d %H:%M:%S'
MATCH_DATE = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
MATCH_TIME = r'(\d{2})時(\d{2})分'
MATCH_DATETIME_FORMAT = r'(\d{4})年(\d{1,2})月(\d{1,2})日 (\d{2})時(\d{2})分'

def dash_format(phone_number):
   # Ensure the phone number is a string
   phone_number = str(phone_number)
   phone_number = re.sub(r'\D', '', phone_number)
   
   # Define the regular expression pattern
   pattern = r'^(\d{3})'
   repl = r'\1'
   count = 1
   for i in range(3, len(phone_number), 4):
      num_group = min(len(phone_number[i:]), 4)
      pattern += r'(\d{' + str(num_group) + r'})'
      repl += '-\\' + str(count+1) 
      count += 1

   # Use re.sub() to insert hyphens in the appropriate positions
   formatted_number = re.sub(pattern, repl, phone_number)
   
   return formatted_number

def undash_format(phone_number_dash):
   # Ensure the phone number is a string
   phone_number_dash = str(phone_number_dash)
   phone_number_dash = re.sub(r'\D', '', phone_number_dash)
   
   # Use re.sub() to remove hyphens
   phone_number = re.sub(r'-', '', phone_number_dash)
   
   return phone_number

def only_numbers(number_str):
   return re.sub(r'\D', '', number_str)

def only_alphabets(alpha_str):
   return re.sub(r'\W', '', alpha_str)

def only_alphabets_and_numbers(alpha_num_str):
   return re.sub(r'\W', '', alpha_num_str)

def string_to_datetime(string_date=None, match_format=MATCH_DATETIME_FORMAT):
    # return None if no date string is provided
    if string_date is None:
        return None
    
    # Preprocessing date string
    match_date = re.match(match_format, string_date)
    year = int(match_date.group(1))
    month = int(match_date.group(2)) 
    day = int(match_date.group(3))
    hour = int(match_date.group(4))
    minute = int(match_date.group(5))

    # Get target date and time
    target_datetime = datetime(year, month, day, hour, minute)
    
    return target_datetime

def string_to_date(string_date=None, match_format=MATCH_DATETIME_FORMAT):
      # return None if no date string is provided
      if string_date is None:
         return None
      
      # Preprocessing date string
      match_date = re.match(match_format, string_date)
      year = int(match_date.group(1))
      month = int(match_date.group(2)) 
      day = int(match_date.group(3))
   
      # Get target date and time
      target_date = datetime(year, month, day)
      
      return target_date

def get_jst_datetime():
   # Get current date and time in JST timezone
   current_date_time = datetime.now(JAPAN_TIMEZONE)

   # Convert the date and time to a string
   string_date = current_date_time.strftime(DATETIME_FORMAT)
   match_date = re.match(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})', string_date)
   year = int(match_date.group(1))
   month = int(match_date.group(2)) 
   day = int(match_date.group(3))
   hour = int(match_date.group(4))
   minute = int(match_date.group(5))

   # Get current date and time in JST timezone
   current_date_time = datetime(year, month, day, hour, minute)
   return current_date_time

def get_jst_date():
   # Get current date and time in JST timezone
   current_date_time = datetime.now(JAPAN_TIMEZONE)

   # Convert the date and time to a string
   string_date = current_date_time.strftime(DATETIME_FORMAT)
   match_date = re.match(r'(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})', string_date)
   year = int(match_date.group(1))
   month = int(match_date.group(2)) 
   day = int(match_date.group(3))

   # Get current date and time in JST timezone
   current_date = datetime(year, month, day)
   return current_date

def int_timedelta(datetime1: datetime, datetime2: datetime):
   time_delta = datetime1 - datetime2
   return int(time_delta.total_seconds())


def is_today(time_diff):
      if time_diff < 24 * 60 * 60:
         return True
      return False

if __name__=="__main__":
   phone_number = '0912-3456-789'
   dash_number = dash_format(phone_number)
   undash_number = undash_format(phone_number)
   print(dash_number)
   print(undash_number)

   start_date = '2024年04月16日 23時59分'
   target_date = string_to_date(start_date)
   print(target_date)

   current_jst_date_time = get_jst_date()
   print(current_jst_date_time)

   print(target_date > current_jst_date_time)
   print(target_date - current_jst_date_time)
   int_detla = int_timedelta(target_date, current_jst_date_time)
   print(int_detla)

   print(is_today(int_detla))

   print(get_jst_date())
