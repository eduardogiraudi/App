import { useEffect, useState } from "react"
import authServer from "./settings";
import LoginWithGoogle from "./LoginWithGoogle";
import { Link, useNavigate } from "react-router-dom";


function Register (){
    const [password, setPassword] = useState()
    const [confirmPassword, setConfirmPassword] = useState()
    const [username, setUsername] = useState()
    const [email, setEmail] = useState()
    const [usernameErr, setUsernameErr] = useState()
    const [emailErr, setEmailErr] = useState()
    const [passwordErr, setPasswordErr] = useState()
    const [submitBlock, setSubmitBlock] = useState(true)
    const [err, setErr] = useState() //errori dopo che il form viene inviato
    let navigate = useNavigate()
    const handleSubmit = (e)=>{
        e.preventDefault()
        const body = new FormData(e.currentTarget)
        let url = authServer+'/auth/register'
        fetch(url, {
            method: 'POST',
            body: body
        })
        .then(res=>{
            if(res.status!==200){
                // if(res.status===400) throw new Error('email non valida o password non corrispondente alle policy di sicurezza o le due password non sono identiche')
                if(res.status===400){return res.json().then(err=>{
                    if(err.message==='invalid email'){
                        throw new Error('email non valida')
                    }else{
                        throw new Error('password non valida')
                    }
                })}
                if(res.status===422) throw new Error('l\'utente è già registrato con un account google')
                if(res.status===409) throw new Error('email o username già esistenti nel sistema')
                if(res.status===500) throw new Error('errore interno del sistema, si prega di riprovare la registrazione')
            }
            return res.json()
        })
        .then(data=>{
                navigate('/response',{
                    state: {
                        message: `Gentile ${data.message}, si prega di controllare l'email contenente il link di attivazione account per poter completare il processo di registrazione, se l'email non arriva richiedine una nuova tentando di loggarti`
                    }
                })
                setErr(false); 
        })
        //handliamo gli errori qua settando lo stato err al txt dell'errore
        .catch(error=>setErr(error.message))
    }

    const usernameChange = async (e) => {
        try {
            setUsername(e.target.value)
            let val = e.target.value 
            setUsernameErr()
            if(val){
                if(val.length<5){
                    throw new Error("il nome utente deve essere lungo almeno 5 caratteri")
                }
                let http = await fetch(authServer+'/auth/user_exists?username='+val)
                    .then(res=>res.status);
                if(http === 409){
                    throw new Error('nome utente non disponibile')
                }
            }

        }
        catch(error){
            setUsernameErr(error.message)
        }
    }
    const emailChange = async (e) => {
        try{
            setEmail(e.target.value)
            setEmailErr()
            let val = e.target.value
            if(val){
                if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)){
                    throw new Error('inserire una email valida')
                }
                let http = await fetch(authServer+'/auth/user_exists?email='+val)
                .then(res=>res.status);
                if(http === 409){
                    throw new Error('email non disponibile')
                }
            }

        }catch(error){
            setEmailErr(error.message)
        }
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
        try{
            setConfirmPassword(e.target.value)
            setPasswordErr()
            let val = e.target.value; 
            if(password && val){
                if(password!==val) throw new Error('le due password non coincidono')
                else if(password.length < 8 || !/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-!@#$%^&*()_+`~={}[\]:;"'<>,.?\\/])[A-Za-z\d-!@#$%^&*()_+`~={}[\]:;"'<>,.?\\/]{8,}$/.test(password)){
                    throw new Error('La password deve contenere almeno una lettera maiuscola, una minuscola, un simbolo, un numero e deve essere almeno di 8 caratteri')
                }
            }

        }catch(error){
            setPasswordErr(error.message)
        }
    }

    useEffect(()=>{
        setSubmitBlock(true)
        // se tutti gli input sono completati e non c'è nessun errore
        if((email && username && password && confirmPassword)&& (!emailErr && !usernameErr && !passwordErr)){
            setSubmitBlock(false)
        }            
    },[password, confirmPassword,email,username, emailErr, usernameErr, passwordErr])
    return (
        <>
            <Link to={'/login'}>Hai già un account? Accedi</Link>
            <form onSubmit={handleSubmit}>  
                <input type="text" name='username' placeholder="username" onChange={usernameChange}/>
                {usernameErr&&<div>{usernameErr}</div>}
                <input type="email" name="email" placeholder="email" onChange={emailChange}/>
                {emailErr&&<div>{emailErr}</div>}
                <input type="password" name="password" onChange={handlePasswordChange} placeholder="password"/>
                <input type="password" name="confirm_password" onChange={handleConfirmPasswordChange} placeholder="confirm password"/>
                {passwordErr&&<div>{passwordErr}</div>}
                <input type="submit" disabled={submitBlock?true:false}/>
                {err&&<div>{err}</div>}
            </form>
            <LoginWithGoogle/>
        </>
    )
}export default Register