import os
import requests
import zipfile
import shutil
import time
from typing import List
from setuptools import find_packages, setup
from typing import List

print("Setup started...")
print("Installing requirements...")
time.sleep(1)
# Install the requirements
os.system("pip install -r ./requirements.txt")
print("Requirements installed")

# https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/win64/chromedriver-win64.zip
def unzip_folder_name(zip_url: str):
    return zip_url.split("/")[-1].split(".zip")[0]


# Define the URL for the ChromeDriver download
# get the latest chrome driver version number
CHROME_DRIVER_PATH = "https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/win64/chromedriver-win64.zip"

# Define the destination directory for the ChromeDriver
DRIVER_DIR = "./drivers"
CHROME_DRIVER_DIR = os.path.join(DRIVER_DIR, "chromedriver")
CHROME_UNZIP_DIR = os.path.join(DRIVER_DIR, unzip_folder_name(CHROME_DRIVER_PATH))

# Create the destination directory if it doesn't exist
if not os.path.exists(DRIVER_DIR):
   os.makedirs(DRIVER_DIR)
   print("Created directory: " + DRIVER_DIR)

if os.path.exists(CHROME_UNZIP_DIR):
   shutil.rmtree(CHROME_UNZIP_DIR)
   print("Removed directory: " + CHROME_UNZIP_DIR)

if os.path.exists(CHROME_DRIVER_DIR):
   shutil.rmtree(CHROME_DRIVER_DIR)
   print("Removed directory: " + CHROME_DRIVER_DIR)

os.makedirs(CHROME_DRIVER_DIR)
print("Created directory: " + CHROME_DRIVER_DIR)

# Download the ChromeDriver zip file
response = requests.get(CHROME_DRIVER_PATH)
zip_file_path = os.path.join(DRIVER_DIR, "chromedriver.zip")
with open(zip_file_path, "wb") as zip_file:
   zip_file.write(response.content)
print("Downloaded ChromeDriver zip file")

# Extract the contents of the zip file
with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
   zip_ref.extractall(DRIVER_DIR)
print("Extracted ChromeDriver zip file")

# Remove the zip file
os.remove(zip_file_path)
print("Removed ChromeDriver zip file")

# Move the ChromeDriver executable to the destination directory
for file in os.listdir(CHROME_UNZIP_DIR):
   abs_file_path = os.path.join(CHROME_UNZIP_DIR, file)
   if abs_file_path.endswith(".exe"):
      shutil.move(abs_file_path, CHROME_DRIVER_DIR)
      print("Moved ChromeDriver executable to: " + CHROME_DRIVER_DIR)

shutil.rmtree(CHROME_UNZIP_DIR)
print("Removed directory: " + CHROME_UNZIP_DIR)

print("Setup completed successfully!")
