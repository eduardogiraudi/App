# App


## Requisiti 
Sul computer deve essere installato docker (necessario in fase di sviluppo per creare i container con MongoDB e Redis), Python versione 3.12 (con pipenv) e NodeJS

## Installazione dipendenze
Su sistemi Unix like eseguire il file install, per sistemi Windows eseguire il file install.ps1. Alla fine dell'esecuzione il terminale avrà installato tutte le dipendenze di tutti i server.

## Struttura e funzionamento del backend
Il backend si dividerà in più server, per ora uno di autenticazione (che si occupa di tutto ciò che concerne l'autenticazione e più in generale i dati di accesso degli utenti) fornendo la possibilità di login interno all'app o tramite oAuth con Google, il server di risorse (contenente rotte sia protette che non), l'OTP server, che si occupa della verifica di dispositivi nuovi da parte degli utenti, l'Email server che si occupa di ascoltare le code redis alla chiave email e inviare email. le rotte del resource server saranno protette grazie al fatto che i  server condividono lo stesso file con le variabili d'ambiente contenente la firma server


## Documentazione delle api
### Auth-Server
#### Porta
la porta è 8080
### Resource-Server
#### Porta
la porta è 5001
### OTP-Server
#### Porta
la porta è 5000
### Backup-Database-Bot
bot che alle 3 del mattino esegue un backup del database, dovrà fare poi un backup di tutti i database, seguire poi le istruzioni di dist per il suo deploy
### MongoDB
la sua porta è la standard 27017, per avviarlo è necessario avere Docker, creando il container col comando docker compose (all'interno della directory di root dell'app)
### MongoDB-Backup
la sua porta è 27018, è un database di backup, dovrà fare un backup di tutti i database e il suo microservizio dovrà essere isolato in altro network (per renderlo inaccessibile a tutti)
### Redis
per ora serve per le code email, i vari server pushano nuovi dati in coda e l'email server è in costante ascolto delle chiavi email per mandarle, su windows ci connettiamo con lo script redis-cli.ps1, su mac meglio installarlo. 
#### Porta
la porta è 6380
### Email server
Uno script python vanilla che ascolta in un loop infinito la coda redis cercando nuove chiavi email, quando le trova le deserializza e invia le email con i loro dati, aumenta la scalabilità dei vari server che necessitano l'invio di email in determinate rotte API



## Istruzioni di build e deploy
### Auth-Server
sostituire nell'env react SOLO l'indirizzo dell'auth server a stringa vuota, gli altri indirizzi metterci poi i sottodomini corretti del deploy. su google console andare a cambiare l'url dell'app per autorizzarla all'Oauth. la password di redis è dentro al compose, per cambiarla in build impostartla di li.

### Backup-Database-Bot
creare una cron con crontab -e su terminale e incollarci il percorso assoluto dello script shell run_backup.sh (sostituire all'interno di sto file con il percorso assoluto dell'env, ottenendolo con pipenv --env entrando prima dentro la cartella Backup-Database-Bot) e aggiungerci prima source e dopo il path (attaccato) /bin/activate