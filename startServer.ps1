$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
cd $scriptDir\
$env:FLASK_APP = "app.py"
invoke-expression 'cmd /c start powershell -Command {
Write-Host "Opening website...."
Start-Sleep -s 5
start chrome http://127.0.0.1:5000/}'
Write-Host "Starting web server...."
flask run