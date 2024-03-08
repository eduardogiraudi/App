# Funzione per ottenere il percorso assoluto dello script
function Get-ScriptDir {
    $ScriptPath = $MyInvocation.MyCommand.Path
    $ScriptDir = Split-Path $ScriptPath
    return $ScriptDir
}

# Ottieni il percorso del progetto
$ProjectDir = Get-ScriptDir

# Funzione per aprire un nuovo terminale e eseguire il comando in background
function Open-Terminal($command) {
    Start-Process "cmd.exe" -ArgumentList "/c cd $ProjectDir ; $command" -NoNewWindow
}

Write-Host "Avvio MongoDB e Redis"
Open-Terminal "docker compose up"

Write-Host "Avvio l'email server"
Open-Terminal "cd $ProjectDir\Email-Server; pipenv run python3 app.py"

Write-Host "Avvio il server di autenticazione"
Open-Terminal "cd $ProjectDir\Auth-Server; cd login; npm start"
Open-Terminal "cd $ProjectDir\Auth-Server; pipenv run flask --debug run --port 8080"

Write-Host "Avvio il resource server"
Open-Terminal "cd $ProjectDir\Resource-Server; pipenv run flask --debug run --port 5001"

Write-Host "Avvio l'OTP server"
Open-Terminal "cd $ProjectDir\Auth-Server; cd otp; npm start"
Open-Terminal "cd $ProjectDir\OTP-Server; cd otp; npm start; pipenv run flask --debug run"

Write-Host "Tutti i server avviati"
