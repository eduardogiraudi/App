#!/bin/bash
#mettere il percorso assoluto di sto file dopo aver aperto un terminale e aver fatto crontab -e: * * * * * /percorso/assoluto/del/tuo/run_backup.sh (fare il chmod prima)
# per eseguirlo ogni giorno alle 3 del mattino (meno traffico di rete per il backup così) fare: 0 3 * * * /percorso/assoluto/del/tuo/run_backup.sh (fare il chmod +x prima)
# Naviga nella directory del tuo script Python
cd /Users/eduz/App/Backup-Database-Bot/
VIRTUAL_ENV=ddd #sostituirlo poi con il path dell'ambiente virtuale reale in dist, lo si vede entrando nella cartella e facendo pipenv --venv, si aggiunge prima source e alla fine bin/activate 
source /Users/eduz/.local/share/virtualenvs/Backup-Database-Bot-NCGd4QkM/bin/activate
python3 app.py

deactivate
echo "done"
