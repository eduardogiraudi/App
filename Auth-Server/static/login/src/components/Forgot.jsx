function Forgot(){
    // questo fa un fetch e comunica al db che l'utente ha richiesto un cambio password, il server invia mail con itsdangerous che crea 
    //un id univoco e il link punterà a una route react con il form, che estrare i query parameters e li usa per verificare se il link 
    //è scaduto o meno, se non lo è mostra un form con password e conferma password che manderanno una POST che modificherà la password
    return (
        <input type="email" name="email" id="email" />
    )
}export default Forgot