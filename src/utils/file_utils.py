import yaml
import json
from typing import Any

from src.exceptions import BaseException

def read(file: str) -> Any:
   if file.endswith('.yml'):
      return read_yml(file)
   elif file.endswith('.json'):
      return read_json(file)
   else:
      try:
         with open(file, 'r', encoding='utf-8') as stream:
            return stream.read()
      except Exception as exc:
         BaseException.raise_exc(exc)
         return None

def write(file: str, data) -> None:
   if file.endswith('.yml'):
      write_yml(file, data)
   elif file.endswith('.json'):
      write_json(file, data)
   else:
      try:
         with open(file, 'w', encoding='utf-8') as stream:
            stream.write(data)
      except Exception as exc:
         BaseException.raise_exc(exc)
   
def read_yml(yml_file: str) -> Any:
   try:
      with open(yml_file, 'r', encoding='utf-8') as stream:
         return yaml.safe_load(stream)
   except Exception as exc:
      BaseException.raise_exc(exc)
      return None
      
def write_yml(yml_file: str, data) -> None:
   try:
      with open(yml_file, 'w', encoding='utf-8') as stream:
         yaml.dump(data, stream)
   except Exception as exc:
      BaseException.raise_exc(exc)

def read_json(json_file: str) -> Any:
   try:
      with open(json_file, 'r', encoding='utf-8') as stream:
         return json.load(stream)
   except Exception as exc:
      BaseException.raise_exc(exc)
      return None

def write_json(json_file: str, data) -> None:
   try:
      with open(json_file, 'w', encoding='utf-8') as stream:
         json.dump(data, stream)
   except Exception as exc:
      BaseException.raise_exc(exc)


if __name__=="__main__":
   file = "data.yml"
   data = read_yml(file)