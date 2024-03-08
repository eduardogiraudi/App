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

Write-Host "Installo le dipendenze"
Set-Location "$ProjectDir\Email-Server"
pipenv install
Set-Location "$ProjectDir"

Set-Location "$ProjectDir\Auth-Server"
pipenv install
Set-Location "$ProjectDir\login"
npm install
Set-Location "$ProjectDir"

Set-Location "$ProjectDir\OTP-Server"
pipenv install
Set-Location "$ProjectDir\otp"
npm install
Set-Location "$ProjectDir"

Set-Location "$ProjectDir\Resource-Server"
pipenv install
Set-Location "$ProjectDir\app"
npm install
Set-Location "$ProjectDir"

# Attendi un po' prima di avviare il server successivo
Write-Host "Dipendenze installate"
