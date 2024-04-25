import logging
from datetime import datetime
from src.utils import storage_manage as sm
from src.globals import Paths, Variables

class Levels:
   INFO = logging.INFO
   WARNING = logging.WARNING
   ERROR = logging.ERROR
   DEBUG = logging.DEBUG

class Names:
   ROOT_LOG = "root"
   MAIN_CONTROLLER = "main_controller"
   FILLER = "filler"
   FINDER = "finder"


class BaseLogger:
   parent_folder = sm.path_join(Paths.logs, Variables.date)
   child_folder = sm.path_join(parent_folder, Variables.current_time)

   def __init__(self, log_name: str = Names.MAIN_CONTROLLER, max_durations: int = 10) -> None:
      # init log folder and log files
      self.log_name = log_name
      log_file_path = sm.path_join(BaseLogger.child_folder, log_name + ".log")
      root_log_path = sm.path_join(BaseLogger.child_folder, Names.ROOT_LOG + ".log")

      print(f"Log file path: {log_file_path}")

      # Create log folder if it does not exist
      sm.create_dirs(BaseLogger.parent_folder, BaseLogger.child_folder)
      sm.create_files(log_file_path, root_log_path)

      # Logging configuration for this logger instance
      self.logger = logging.getLogger(log_name)

      formatter = logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s")

      file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
      file_handler.setFormatter(formatter)
      self.logger.addHandler(file_handler)

      # Logging configuration for the root logger
      logging.basicConfig(
         format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
         level = logging.INFO, 
         handlers=[logging.FileHandler(root_log_path, encoding="utf-8")]
      )   

      # Remove old log files and folders
      self._manage_log_folders(Paths.logs, max_num=max_durations)
      self._manage_log_folders(BaseLogger.parent_folder, max_num=max_durations)
   
   def _manage_log_folders(self, log_folder: str, max_num: int = 10):
      try:
         # Get a list of all log folders
         log_dirs = sm.list_dirs(log_folder)
         # If there are more than max_num log folders, delete the oldest ones
         if len(log_dirs) > max_num:
            sorted_dirs = sorted(log_dirs)
            sm.remove_all_dirs(sorted_dirs[:-max_num])
      except Exception as e:
         self.exception("Caught exception while managing log folders", str(e))

   def info(self, *msg:str) -> None:
      self._log(logging.INFO, *msg)

   def warning(self, *msg:str) -> None:
      self._log(logging.WARNING, *msg)

   def error(self, *msg:str) -> None:
      self._log(logging.ERROR, *msg)

   def debug(self, *msg:str) -> None:
      self._log(logging.DEBUG, *msg)

   def exception(self, *msg:str) -> None:
      self.logger.exception(" ".join(msg))
      ins_message = f"{logging.getLevelName(logging.ERROR).upper()} - {msg}"
      self.ins(ins_message)

   def ins(self, *msg:str) -> None:
      message = " ".join(msg)
      print_text = f"{self.log_name} - {message}"
      log_text = f"[ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ] {print_text}"
      print(log_text)

   def _log(self, level: int, *msg:str) -> None:
      message = " ".join(msg)
      self.logger.log(level, message)
      ins_message = f"{logging.getLevelName(level).upper()} - {message}"
      self.ins(ins_message)

   @staticmethod
   def get(log_name: str = Names.MAIN_CONTROLLER) -> 'BaseLogger':
      return BaseLogger(log_name)

# testing
if __name__=="__main__":
   main_logger = BaseLogger.get(Names.MAIN_CONTROLLER)
   main_logger.info("This is an info message", "from the logger")
   main_logger.ins("This is an instance message", "from the logger", "that is just printed to the console")
   filler_logger = BaseLogger.get(Names.FILLER)
   filler_logger.info("This is an info message", "from the filler logger")
