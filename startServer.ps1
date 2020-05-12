$scriptDir = Split-Path -Path $MyInvocation.MyCommand.Definition -Parent
cd $scriptDir\
venv/Scripts/activate
$env:FLASK_APP = "app.py"
invoke-expression 'cmd /c start powershell -Command {
Start-Sleep -s 10
start chrome http://127.0.0.1:5000/}'
flask run