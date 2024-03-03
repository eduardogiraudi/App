import { Link, useLocation, useNavigate } from "react-router-dom";
import {authServer} from "./settings";
import { useEffect, useState } from "react";

// far gestire a flask l'authorization header, è più sicuro così
function ChangePassword (){
    const [password, setPassword] = useState()
    const [confirmPassword, setConfirmPassword] = useState()
    const [passwordErr, setPasswordErr] = useState()
    const [preventSubmit, setPreventSubmit] = useState(true)
    const [err, setErr] = useState(false)
    const location = useLocation();
    const queryParameters = new URLSearchParams(location.search);
    const token = queryParameters.get('token');
    let navigate = useNavigate()

    const handleSubmit = (e)=>{

        e.preventDefault(); 
        let body = new FormData(e.currentTarget)
        body.append('token', token)
        const url = authServer + '/auth/reset_password'
        fetch(url, {
            method:'POST',
            body: body
        })
        .then(
            res=>{
                if(res.status===200) {
                    navigate('/response',{
                        state: {
                            message: 'Password cambiata con successo'
                        }
                    })
                }
                if(res.status===400) throw new Error('le password non coincidono o non corrispondono alle policy di sicurezza')
                if(res.status===410) throw new Error('il link è scaduto, si prega di richiederne uno nuovo')
                if(res.status===401) throw new Error('il link non è valido, si prega di ricontrollare e/o richiederne uno nuovo')
                if(res.status===404) throw new Error('utente non trovato')
            }
        )
        .catch(err=>{
            setErr(err.message)
        })
        
    }
    const handlePasswordChange = (e) =>{    
        // val serve per avere il valore dello stato subito (se verifichiamo il valore dello state quando lo abbiamo appena settato avremo ancora il prcedente, è asincrono il suoset)
        try{
            setPassword(e.target.value)
            setPasswordErr()
            let val = e.target.value; 
            if(val && confirmPassword){
                if(val!==confirmPassword) throw new Error('le due password non coincidono')
                else if(val.length < 8 || !/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-!@#$%^&*()_+`~={}[\]:;"'<>,.?\\/])[A-Za-z\d-!@#$%^&*()_+`~={}[\]:;"'<>,.?\\/]{8,}$/.test(val)){
                    throw new Error('La password deve contenere almeno una lettera maiuscola, una minuscola, un simbolo, un numero e deve essere almeno di 8 caratteri')
                }
            }

        }catch(error){
            setPasswordErr(error.message)
        }
    }
    const handleConfirmPasswordChange = (e) =>{    
        // val serve per avere il valore dello stato subito (se verifichiamo il valore dello state quando lo abbiamo appena settato avremo ancora il prcedente, è asincrono il suoset)
        try{
            setConfirmPassword(e.target.value)
            setPasswordErr()
            let val = e.target.value; 
            if(val && password){
                if(val!==password) throw new Error('le due password non coincidono')
                else if(val.length < 8 || !/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-!@#$%^&*()_+`~={}[\]:;"'<>,.?\\/])[A-Za-z\d-!@#$%^&*()_+`~={}[\]:;"'<>,.?\\/]{8,}$/.test(val)){
                    throw new Error('La password deve contenere almeno una lettera maiuscola, una minuscola, un simbolo, un numero e deve essere almeno di 8 caratteri')
                }
            }

        }catch(error){
            setPasswordErr(error.message)
        }
    }

    useEffect(()=>{
        setPreventSubmit(true)
        if(password && confirmPassword && !passwordErr){
            setPreventSubmit(false)
        }
    },[password, confirmPassword, passwordErr])
    return (
        <>
            {!token&&<div>Sembra che il link non sia valido, ricontrolla la mail o richiedine uno nuovo</div>}
            {token&&<form onSubmit={handleSubmit}>
                <input type="password" name="password" placeholder="password" onChange={handlePasswordChange}/>
                <input type="password" name="confirm_password" placeholder="confirm password" onChange={handleConfirmPasswordChange}/>
                {passwordErr&&<div>{passwordErr}</div>}
                <input type="submit" disabled={preventSubmit?true:false}/>
            </form>}
            {err&&<div>{err}</div>}
        <Link to={'/login'}>torna al Login</Link>
        </>
    )
}
export default ChangePassword