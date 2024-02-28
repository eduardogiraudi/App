# App
## Struttura e funzionamento del backend
Il backend si dividerà in più server, per ora uno di autenticazione (che si occupa di tutto ciò che concerne l'autenticazione e più in generale i dati di accesso degli utenti) fornendo la possibilità di login interno all'app o tramite oAuth con Google, il server di risorse (contenente rotte sia protette che non) e l'OTP server, che si occupa della verifica di dispositivi nuovi da parte degli utenti. le rotte del resource server saranno protette grazie al fatto che i  server condividono lo stesso file con le variabili d'ambiente contenente la firma server


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
### MongoDB
la sua porta è la standard 27017, per avviarlo è necessario avere docker, creando il container col comando docker compose (all'interno della directory Auth-Server)