$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent

Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
choco install -f -y python
cd $scriptDir\
py -3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt