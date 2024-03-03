import { Link, useLocation } from "react-router-dom";
import authServer from "./settings";
import { useEffect, useState } from "react";
// far gestire a flask l'authorization header, è più sicuro così
function ActivateAccount (){
    const [loading, setLoading] = useState(true)
    const [response, setResponse] = useState()
    const [error, setError] = useState() // semplicemente per togglare gli stili css in seguito
    const location = useLocation();
    const queryParameters = new URLSearchParams(location.search);
    const token = queryParameters.get('token')
    let formData = new FormData()
    formData.append('token',token)

    //richiesta senza parametri, account già attivato, account attivato con successo
    useEffect(()=>{
        fetch(authServer+'/auth/activate_account',{
            method:'POST',
            body: formData
        })
        .then(res=>{
            setLoading(false)
            if(res.status===200) setResponse('Account attivato con successo')
            if(res.status===400) throw new Error('La richiesta era incompleta, sei sicuro di aver copiato correttamente l\'URL di attivazione?')
            if(res.status===409) throw new Error('L\'account è già stato attivato')
            if(res.status===410) throw new Error('il link di attivazione è scaduto, richiedine uno nuovo loggandoti')
            if(res.status===401) throw new Error('il link di attivazione non è valido o non è del tutto completo')
            if(res.status===404) throw new Error('utente inesistente')
            
        })
        .catch((err)=>{
            setResponse(err.message)
            setError(true)
        })
    })
    return (
        <>  
            <Link to={'/login'}>torna al Login</Link>
            {!token&& <div>Sembra che il link non sia valido, ricontrolla la mail o richiedine uno nuovo loggandoti</div>}
            {loading && token&& <div>Loading...</div>}
            {response && token && <div style={{'background':error?'red':'green'}}>{response}</div>}

        </>
    )
}
export default ActivateAccount