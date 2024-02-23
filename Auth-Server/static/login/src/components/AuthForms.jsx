import { useState } from "react"
import {BrowserRouter as Router} from 'react-router-dom'
import { Route, Routes, Link } from "react-router-dom";
import ChangePassword from "./ChangePassword";
import Forgot from "./Forgot";
import Login from "./Login";
import LoginWithGoogle from "./LoginWithGoogle";
import Register from "./Register";
import authServer from "./settings";
function AuthForms(){
    const [loginRegisterForgot, setLoginRegisterForgot] = useState('login') 
    const [err, setErr] = useState(false);
    const [success, setSuccess] = useState(false); 
    const [submitBlock, setSubmitBlock] = useState(true)
    const [specialPage, setSpecialPage] = useState(false) // se è true elimina parti della pagina (ad esempio se l'utente si registra si mostra solo il messaggio di successo e non di nuovo il form di registrazione)







    const handleSubmit = (e)=>{
        e.preventDefault()
        const body = new FormData(e.currentTarget)
        //sistemare la recovery di forgot
        let url = loginRegisterForgot==='register'?authServer+'/auth/register'
                    :loginRegisterForgot==='login'?authServer+'/auth/login'
                    :authServer+'/auth/forgot_password'
        fetch(url, {
            method: 'POST',
            body: body
        })
        .then(res=>{
            if(res.status!==200){
                if(loginRegisterForgot==='login'){
                    setSuccess(false);
                    if(res.status === 401){
                        throw new Error('Password non corretta')
                    }else if(res.status === 404){
                        throw new Error('Utente non trovato o form non compilato correttamente')
                    }
                }else if(loginRegisterForgot==='forgot'){
                    setSuccess(false);
                    if(res.status ===404){
                        throw new Error('Purtroppo non abbiamo trovato il tuo utente, si prega di controllare e reinserire l\'email corretta'); 
                    }else if(res.status === 400){
                        throw new Error('Non hai completato il form di reset password e la richiesta di reset non può essere inoltrata')
                    }
                }else if(loginRegisterForgot==='register'){
                    setSuccess(false);
                    throw new Error('Si prega di riprovare a registrarsi compilando tutti i form'); 
    
                }
            }
            return res.json()
        })
        .then(data=>{
            if(loginRegisterForgot==='login'){ // ci stiamo loggando
                document.cookie = `token=${data.message.token}`
                document.cookie = `refresh_token=${data.message.refresh_token}`
                // redirectare in homepage (il frontend del resource server)
                // window.location.href = 'http://localhost:8080/'
                console.log(data);

                // gestire il comportamento di login poi, con un redirect al resource server
                setSuccess(true);
                setErr(false); 
    
            }else if(loginRegisterForgot==='register'){
                setSuccess('Account creato, si prega di controllare l\'email contenente il link di attivazione account per poter utilizzare il servizio');
                setErr(false); 
                
            }else if(loginRegisterForgot==='forgot'){
                setSuccess(true);
                setErr(false); 
            }
        })
        //handliamo gli errori qua settando lo stato err al txt dell'errore
        .catch(error=>setErr(error.message))
    }
    return (
        <>
            <Router>
                <Link
                to={
                    loginRegisterForgot==='register'?'/login'
                    :loginRegisterForgot==='login'?'/register'
                    :'/login'
                }   
                onClick={() => {
                    setLoginRegisterForgot(loginRegisterForgot === 'register' ? 'login' : loginRegisterForgot === 'login' ? 'register' : 'login');
                }}                
                >
                    {
                        loginRegisterForgot==='register'?'Hai già un account? Accedi'
                        :loginRegisterForgot==='login'?'Non hai un account? Registrati'
                        :'Torna al login'
                    }
                </Link>
                    <Routes>
                        <Route path="/" element={<form onSubmit={handleSubmit}><Login/><input type="submit"/></form>}/>
                        <Route path="/login" element={<form onSubmit={handleSubmit}><Login/><input type="submit"/></form>}/>
                        <Route path="/register" element={<form onSubmit={handleSubmit}><Register setErr={setErr} setSubmitBlock={setSubmitBlock}/><input type="submit" disabled={submitBlock?true:false}/></form>}/>
                        <Route path="/forgot" element={<form onSubmit={handleSubmit}><Forgot/><input type="submit"/></form>}/>
                        <Route path="/change_password" element={<ChangePassword/>}/>
                        <Route path="/activate_account" element='ciao'/>
                    </Routes>
                {success&&<div>{success}</div>}
                {err&&<div>{err}</div>}
                {loginRegisterForgot === 'login' && <Link to='/change_password' onClick={()=>{setLoginRegisterForgot('forgot')}}>Hai dimenticato la password? Ripristinala</Link> }
                {(loginRegisterForgot==='login'||loginRegisterForgot==='register')&&<LoginWithGoogle/>}
            </Router>
        </>
    )
}
export default AuthForms