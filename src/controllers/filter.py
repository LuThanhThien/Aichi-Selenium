from typing import List, Union
import enum

from src.globals import Meta
from src.models.account import Account
from src.models.form import FormInfo
from src.models.form import FormInfoAttr as Att
from .base_controller import BaseController

class FilterMode(enum):
   '''    Filter mode    '''
   Contains = "contains"
   NotContains = "not_contains"
   Equals = "equals"
   NotEquals = "not_equals"
   GreaterThan = "greater_than"
   LessThan = "less_than"

class FilterLayer:
   '''    Filter layer    '''
   
   class ANY:
      '''    ANY    '''
      def __init__(self, *args: 'FilterLayer') -> None:
         self.args = args

      def apply(self, form_info: FormInfo) -> Union[FormInfo, None]:
         temp = False
         for arg in self.args:
            result = arg.apply(form_info)
            if result:
               temp = True
         return temp
      
   class ALL:
      '''    ALL    '''
      def __init__(self, *args: 'FilterLayer') -> None:
         self.args = args

      def apply(self, form_info: FormInfo) -> Union[FormInfo, None]:
         for arg in self.args:
            result = arg.apply(form_info)
            if not result:
               return False
         return True
      
   def __init__(self, key: str, value: str, mode: FilterMode) -> None:
      self.key = key
      self.value = value
      self.mode = mode

   def apply(self, form_info: object) -> bool:
      if self.mode == FilterMode.Contains:
         if self.value in getattr(form_info, self.key):
            return True
      elif self.mode == FilterMode.NotContains:
         if self.value not in getattr(form_info, self.key):
            return True
      elif self.mode == FilterMode.Equals:
         if self.value == getattr(form_info, self.key):
            return True
      elif self.mode == FilterMode.NotEquals:
         if self.value != getattr(form_info, self.key):
            return True
      elif self.mode == FilterMode.GreaterThan:
         if self.value > getattr(form_info, self.key):
            return True
      elif self.mode == FilterMode.LessThan:
         if self.value < getattr(form_info, self.key):
            return True
      return False
      
class Filter(BaseController):
   '''    Filter    '''
   def __init__(self, account: Account = None) -> None:
      super().__init__(account)
      self.layers: List[FilterLayer] = []

   def add_layer(self, filter_layer: FilterLayer) -> None:
      if isinstance(filter_layer, FilterLayer)\
         or isinstance(filter_layer, Filter.ANY)\
         or isinstance(filter_layer, Filter.ALL):
         self.layers.append(filter_layer)
      elif isinstance(filter_layer, list):
         for layer in filter_layer:
            self.add_layer(layer)
      else:
         self.logger.error("Invalid filter layer index [{}]: {}".format(len(filter_layer), filter_layer))

   def remove_layer(self, index: int) -> None:
      if 0 <= index < len(self.layers):
         self.layers.pop(index)

   def apply(self, list_form_info: List[FormInfo]) -> List[FormInfo]:
      filtered_list = []
      for form_info in list_form_info:
         for layer in self.layers:
            result = layer.apply(form_info)
            if not result:
               continue
            filtered_list.append(form_info)
      return filtered_list
   
   @staticmethod
   def decide_filter():
      if Meta.keyword == "Tosan":
         return TosanFilter()
      elif Meta.keyword == "Hirabari":
         return HirabariFilter()
      else:
         return Filter()


class HirabariFilter(Filter):
   def __init__(self, account: Account = None) -> None:
      super().__init__(account)
      self.add_layer([
         FilterLayer.ANY(
            FilterLayer(Att.IS_ENDED_STATUS, True, FilterMode.NotEquals),
            FilterLayer.ALL(
               
            )
         )
      ])


class TosanFilter(Filter):
   def __init__(self, account: Account = None) -> None:
      super().__init__(account)
      self.add_layer([
         FilterLayer("status", "ended", FilterMode.NotEquals),
         FilterLayer("status", "passed", FilterMode.NotEquals),
         FilterLayer("status", "upcoming", FilterMode.NotEquals),
         FilterLayer("status", "about_to_close", FilterMode.NotEquals),
         FilterLayer("is_past", True, FilterMode.NotEquals),
         FilterLayer("is_today", True, FilterMode.NotEquals),
      ])

      

   