function Get-ScriptDirectory {
    $scriptPath = $MyInvocation.MyCommand.Path

    if (-not $scriptPath) {
        $scriptPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($MyInvocation.MyCommand.Definition)
    }

    $scriptDirectory = Split-Path $scriptPath
    return $scriptDirectory
}


$scriptDirectory = Get-ScriptDirectory

Start-Process powershell -WorkingDirectory $scriptDirectory -ArgumentList "-NoExit", "-Command", "docker-compose up" 
Start-Process powershell -WorkingDirectory $scriptDirectory -ArgumentList "-NoExit", "-Command", "cd Auth-Server; pipenv run flask --debug run --port 8080" 
Start-Process powershell -WorkingDirectory $scriptDirectory -ArgumentList "-NoExit", "-Command", "cd Auth-Server/login; npm start" 
Start-Process powershell -WorkingDirectory $scriptDirectory -ArgumentList "-NoExit", "-Command", "cd Auth-Server/login/src/css; sass --watch index.scss:index.css" 
Start-Process powershell -WorkingDirectory $scriptDirectory -ArgumentList "-NoExit", "-Command", "cd Resource-Server; pipenv run flask --debug run --port 5001" 
Start-Process powershell -WorkingDirectory $scriptDirectory -ArgumentList "-NoExit", "-Command", "cd Resource-Server/app; npm start;" 
Start-Process powershell -WorkingDirectory $scriptDirectory -ArgumentList "-NoExit", "-Command", "cd Resource-Server/app/src/css; sass --watch index.scss:index.css"
exit; 