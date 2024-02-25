import { useState } from "react"
import authServer from "./settings"
import { Link } from "react-router-dom"

function Forgot(){
    const [err, setErr] = useState()
    const [preventSubmit, setPreventSubmit] = useState(true)
    const [emailErr, setEmailErr] = useState()
    const handleSubmit = (e)=>{
        e.preventDefault()
        const body = new FormData(e.currentTarget)
        //sistemare la recovery di forgot
        let url = authServer+'/auth/forgot_password'
        fetch(url, {
            method: 'POST',
            body: body
        })
        .then(res=>{
            if(res.status!==200){
                    if(res.status ===404){
                        throw new Error('utente non trovato'); 
                    }else if(res.status === 400){
                        throw new Error('si prega di completare il form di reset per poter completare l\'azione')
                    }
            }
            return res.json()
        })
        .then(data=>{
                setErr(false); 
                //fa qualcosa pagina di successo
        })
        //handliamo gli errori qua settando lo stato err al txt dell'errore
        .catch(error=>setErr(error.message))
    }
    const emailChange = async (e) => {
        try{
            setEmailErr()
            let val = e.target.value
            if(val){
                if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)){
                    throw new Error('inserire una email valida')
                }
                setPreventSubmit(false)
            }

        }catch(error){
            setEmailErr(error.message)
            setPreventSubmit(true)
        }
    }
    return (
        <>
            <Link to={'/login'}>Torna al login</Link>
            <form onSubmit={handleSubmit}>
                <input type="email" name="email" id="email" placeholder="email" onChange={emailChange}/>
                {emailErr&&<div>{emailErr}</div>}
                <input type="submit" disabled={preventSubmit?true:false}/>
            </form>
            {err&&<div>{err}</div>}
        </>
    )
}export default Forgot