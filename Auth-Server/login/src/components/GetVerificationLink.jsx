import { useState } from "react"
import authServer from "./settings"
import { Link, useNavigate } from "react-router-dom"

function GetVerificationLink(){
    const [err, setErr] = useState()
    const [preventSubmit, setPreventSubmit] = useState(true)
    const [emailErr, setEmailErr] = useState()
    let navigate = useNavigate()

    const handleSubmit = (e)=>{
        e.preventDefault()
        const body = new FormData(e.currentTarget)

        let url = authServer+'/auth/get_new_verification_link'
        fetch(url, {
            method: 'POST',
            body: body
        })
        .then(res=>{
            if(res.status!==200){
                    if(res.status === 404) throw new Error('utente non trovato')
                    // if(res.status === 400) throw new Error('si prega di completare il form di reset per poter completare l\'azione')
                    if(res.status === 422) throw new Error('il tuo account è legato al tuo account Google, non puoi richiedere un link di verifica')
                    if(res.status === 400) {
                        return res.json().then(error=>{
                            if(error.message==='account is already active') throw new Error('l\'account è già attivato')
                            else if(error.message==='no email provided') throw new Error('non hai fornito un\'email o l\'email non è valida')
                        
                        })
                    }
                    if(res.status === 500) throw new Error('errore interno, se il problema persiste riprovare più tardi')
            }
            return res.json()
        })
        .then(data=>{
                setErr(false); 
                navigate('/response',{
                    state: {
                        message: 'Email di verifica inviata, hai 24 ore per utilizzare il link fornito'
                    }
                })
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
}export default GetVerificationLink