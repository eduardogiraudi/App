# Assicurati di essere nella cartella giusta
cd OTP-Server\

# Avvia flask run in background
$flask_job = Start-Process -NoNewWindow -FilePath "pipenv" -ArgumentList "run", "flask", "--debug", "run", "--port", "5002" -PassThru



# Cambia directory al login
cd otp\

# Avvia npm start in background
pnpm run start-windows


