from src.utils import data_utils as du
from src.globals import URLs
import re

DEFAULT_TITLE = 'title'
DEFAULT_STATUS = 'status'
DEFAULT_START_DATE_STR = '2000年1月1日 00時00分'
DEFAULT_END_DATE_STR = '2100年1月1日 00時00分'
DEFAULT_TEMPLATE_SEQ = 0
DEFAULT_URL = URLs.form_prefix_url + str(DEFAULT_TEMPLATE_SEQ)
DEFAULT_IS_OPEN = False
DEFAULT_IS_PAST = False

class FormStatus:
   UPCOMING = "近日受付開始"
   PASSED = "受付終了しました" 
   ABOUT_TO_CLOSE = "もうすぐ終了"
   ENDED = "終了しました"

class DateLabel:
   START_DATE = "受付開始日時"
   END_DATE = "受付終了日時"

class AccessMessage:
   CLOSED = "大変申し訳ございません。申込数が上限に達した為、締め切らせていただきました。"
   UPCOMING = "申込期間ではありません。"
   OPENED = None

class EndMessage:
   SUCCESS = "申込みが完了しました。"
   FILLED_ALREADY = "既に申込み済みです。"
   DEFENSE_ERROR = "整理番号・パスワードをメモなどにお控えいただくか"
   FALSE = None

class FormInfoAttr:
   TITLE = 'title'
   STATUS = 'status'
   START_DATE_STR = 'start_date_str'
   END_DATE_STR = 'end_date_str'
   TEMPLATE_SEQ = 'template_seq'
   URL = 'url'
   START_DATETIME = 'start_datetime'
   END_DATETIME = 'end_datetime'
   START_DATE = 'start_date'
   END_DATE = 'end_date'
   DATETIME_DIFF = 'datetime_diff'
   DATE_DIFF = 'date_diff'
   IS_PAST = 'is_past'
   IS_PASSED_STATUS = 'is_passed_status'
   IS_UPCOMING_STATUS = 'is_upcoming_status'
   IS_ABOUT_TO_CLOSE_STATUS = 'is_about_to_close_status'
   IS_ENDED_STATUS = 'is_ended_status'
   IS_TODAY = 'is_today'
   IS_NOT_TODAY = 'is_not_today'
   IS_FILLED = 'is_filled'
   IS_CLOSED = 'is_closed'


class FormInfo:
   def __init__(self,
               title: str = DEFAULT_TITLE,
               status: str = DEFAULT_STATUS,
               start_date_str: str = DEFAULT_START_DATE_STR,
               end_date_str: str = DEFAULT_END_DATE_STR,
               template_seq: str = DEFAULT_TEMPLATE_SEQ,
               ) -> None:
      self.title = title
      self.status = status
      self.start_date_str = start_date_str if re.match(du.MATCH_DATETIME_FORMAT, start_date_str) else DEFAULT_START_DATE_STR
      self.end_date_str = end_date_str if re.match(du.MATCH_DATETIME_FORMAT, end_date_str) else DEFAULT_END_DATE_STR
      self.template_seq = template_seq

      self.url = FormInfo.get_url(self.template_seq)
      self.start_datetime = du.string_to_datetime(self.start_date_str)
      self.end_datetime = du.string_to_datetime(self.end_date_str)
      self.start_date = du.string_to_date(self.start_date_str)
      self.end_date = du.string_to_date(self.end_date_str)
      self.datetime_diff = du.int_timedelta(du.get_jst_datetime(), self.start_datetime)
      self.date_diff = du.int_timedelta(du.get_jst_date(), self.start_date)
      
      self._past = self.datetime_diff < 0
      self._filled = False
      self._closed = False
   
   @staticmethod
   def get_url(temp_seq: int = DEFAULT_TEMPLATE_SEQ):
      return URLs.form_prefix_url + str(temp_seq)
   
   @staticmethod
   def default_form():
      return FormInfo()

   def set_filled(self):
      self._filled = True

   def set_closed(self):
      self._closed = True

   @property
   def is_past(self):
      return self._past
   
   @property
   def is_passed_status(self):
      return self.status == FormStatus.PASSED
   
   @property
   def is_upcoming_status(self):
      return self.status == FormStatus.UPCOMING
   
   @property
   def is_about_to_close_status(self):
      return self.status == FormStatus.ABOUT_TO_CLOSE
   
   @property
   def is_ended_status(self):
      return self.status == FormStatus.ENDED
   
   @property
   def is_today(self):
      if abs(self.date_diff) < 24 * 60 * 60:
         return True
      return False
   
   @property
   def is_not_today(self):
      return not self.is_today

   @property
   def is_filled(self):
      return self._filled
   
   @property
   def is_closed(self):
      return self._closed

   def __str__(self) -> str:
      return f"{self.title} - {self.status} - {self.start_date_str} - {self.end_date_str} - {self.template_seq} - {self.url} - {self.is_past}"
   


