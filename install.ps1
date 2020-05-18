$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
Write-Host "Installing virtual environment...."
cd $scriptDir\
py -3 -m venv venv
Write-Host "Activating virtual environment...."
venv\Scripts\activate
pip install -r requirements.txt
Read-Host -Prompt "Press Enter to exit"
