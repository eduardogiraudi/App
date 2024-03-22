# Assicurati di essere nella cartella giusta
cd Resource-Server\

# Avvia flask run in background
$flask_job = Start-Process -NoNewWindow -FilePath "pipenv" -ArgumentList "run", "flask", "--debug", "run", "--port", "5001" -PassThru



# Cambia directory al login
cd app\

# Avvia npm start in background
npm run start-windows


