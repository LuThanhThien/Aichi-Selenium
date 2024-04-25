@REM  Get the current path folder
set current_path=%cd%
echo "Current path folder: $current_path"

@REM  Move to the AichiSelenium folder
cd AichiSelenium
echo "Moved to AichiSelenium folder"s

@REM # Run AichiSelenium main app
echo "Running AichiSelenium main app"
C:\Users\USER\anaconda3\envs\aichi\python.exe -m src.app
echo "AichiSelenium main app finished"
