# Assicurati di essere nella cartella giusta
cd Auth-Server\

# Avvia flask run in background
$flask_job = Start-Process -NoNewWindow -FilePath "pipenv" -ArgumentList "run", "flask", "--debug", "run", "--port", "8080" -PassThru



# Cambia directory al login
cd login\

# Avvia npm start in background
npm run start-windows


