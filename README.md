# App
## Struttura e funzionamento del backend
Il backend si dividerà in 2 server, uno di autenticazione (che si occuperà di fornire token JWT) fornendo la possibilità di login interno all'app o tramite oAuth con Google e il server di risorse (contenente rotte sia protette che non). le rotte del resource server saranno protette grazie al fatto che i due server condividono lo stesso file con le variabili d'ambiente contenente la firma server


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