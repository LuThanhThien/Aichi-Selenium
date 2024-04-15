import os
import glob
import shutil 
   
def path_join(*args) -> str:
   """Join multiple path components intelligently."""
   return os.path.join(*args)

def create_dir(folder_path: str) -> None:
   """Create a folder if it does not exist."""
   if not os.path.exists(folder_path):
      os.makedirs(folder_path)
      print(f"Folder '{folder_path}' created.")
   else:
      print(f"Folder '{folder_path}' already exists.")
      
def create_file(file_path: str) -> None:
   """Create a file if it does not exist."""
   if not os.path.exists(file_path):
      open(file_path, "w").close()
      print(f"File '{file_path}' created.")
   else:
      print(f"File '{file_path}' already exists.")

def delete_dir(dir_path: str) -> None:
   """Delete a dir if it exists."""
   if os.path.exists(dir_path):
      shutil.rmtree(dir_path)
      print(f"dir '{dir_path}' deleted.")
   else:
      print(f"dir '{dir_path}' does not exist.")

def delete_file(file_path: str) -> None:
   """Delete a file if it exists."""
   if os.path.exists(file_path):
      os.remove(file_path)
      print(f"File '{file_path}' deleted.")
   else:
      print(f"File '{file_path}' does not exist.")

def list_dirs(dir_path: str) -> None:
   """List all dirs in the specified directory."""
   dirs = [os.path.join(dir_path, d) for d in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, d))]
   return dirs

def list_files(dir_path: str) -> None:
   """List all files in the specified directory."""
   files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
   return files


def list_files_ends(dir_path: str, ends: str) -> None:
   """List all files in the specified directory that end with the specified string."""
   files = glob.glob(os.path.join(dir_path, f"*{ends}"))
   return files

def rename_dir(old_path: str, new_path: str) -> None:
      """Rename a dir."""
      if os.path.exists(old_path):
         os.rename(old_path, new_path)
         print(f"dir '{old_path}' renamed to '{new_path}'.")
      else:
         print(f"dir '{old_path}' does not exist.")

def move_dir(source_path: str, destination_path: str) -> None:
   """Move a dir to a new location."""
   if os.path.exists(source_path):
         os.rename(source_path, destination_path)
         print(f"dir '{source_path}' moved to '{destination_path}'.")
   else:
         print(f"dir '{source_path}' does not exist.")

def get_dir_size(dir_path: str) -> int:
   """Get the size of a dir in bytes."""
   total_size = 0
   for dirpath, dirnames, filenames in os.walk(dir_path):
         for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
   return total_size

def remove_all_dirs(dirs: list) -> None:
   """Remove all dirs in the list."""
   for dir in dirs:
      delete_dir(dir)

def remove_all_files(files: list) -> None:
   """Remove all files in the list."""
   for file in files:
      delete_file(file)

def is_dir_empty(dir_path: str) -> bool:
   """Check if a dir is empty."""
   return len(os.listdir(dir_path)) == 0

def is_exists(dir_path: str) -> bool:
   """Check if a dir exists."""
   return os.path.exists(dir_path)