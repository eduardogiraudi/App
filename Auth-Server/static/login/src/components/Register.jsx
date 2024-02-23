import { useEffect, useState } from "react"
import authServer from "./settings";
function Register ({setSubmitBlock}){
    const [password, setPassword] = useState()
    const [confirmPassword, setConfirmPassword] = useState()
    const [username, setUsername] = useState()
    const [email, setEmail] = useState()
    const [usernameErr, setUsernameErr] = useState()
    const [emailErr, setEmailErr] = useState()
    const [passwordErr, setPasswordErr] = useState()

    const usernameChange = async (e) => {
        try {
            setUsername(e.target.value)
            let val = e.target.value 
            setUsernameErr()
            if(val){
                let http = await fetch(authServer+'/auth/user_exists?username='+val)
                    .then(res=>res.status);
                if(http === 409){
                    throw new Error('nome utente non disponibile')
                }
                if(val.length<5){
                    throw new Error("il nome utente deve essere lungo almeno 5 caratteri")
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
                let http = await fetch(authServer+'/auth/user_exists?email='+val)
                .then(res=>res.status);
                if(http === 409){
                    throw new Error('email non disponibile')
                }
                if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)){
                    throw new Error('inserire una email valida')
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
            <input type="text" name='username' placeholder="username" onChange={usernameChange}/>
            {usernameErr&&<div>{usernameErr}</div>}
            <input type="email" name="email" placeholder="email" onChange={emailChange}/>
            {emailErr&&<div>{emailErr}</div>}
            <input type="password" name="password" onChange={handlePasswordChange} placeholder="password"/>
            <input type="password" name="confirm_password" onChange={handleConfirmPasswordChange} placeholder="confirm password"/>
            {passwordErr&&<div>{passwordErr}</div>}
        </>
    )
}export default Register