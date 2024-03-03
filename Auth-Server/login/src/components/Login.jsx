import { Link } from "react-router-dom"
import LoginWithGoogle from "./LoginWithGoogle"
import authServer from "./settings";import { useState } from "react";
;
function Login (){
    const [err, setErr] = useState()
    const handleSubmit = (e)=>{
        e.preventDefault()
        const body = new FormData(e.currentTarget)
        let url = authServer+'/auth/login'
        fetch(url, {
            method: 'POST',
            body: body
        })
        .then(res=>{
            if(res.status!==200){
                    if(res.status === 401)throw new Error('password non corretta')
                    if(res.status === 404)throw new Error('utente non trovato o form non compilato correttamente')
                    if(res.status === 422)throw new Error('l\'utente non è ancora verificato')
            }
            return res.json()
        })
        .then(data=>{
                document.cookie = `token=${data.message.token}`
                document.cookie = `refresh_token=${data.message.refresh_token}`
                // redirectare in homepage (il frontend del resource server)
                // window.location.href = 'http://localhost:8080/'
                console.log(data);

                setErr(false); 
    

        })
        .catch(error=>setErr(error.message))
    }
    return (
        <>
            <Link to={'/register'}>Non hai un account? Registrati</Link>
            <form onSubmit={handleSubmit}>
                <input type="text" placeholder="email" name="email"/>
                <input type="password" placeholder="password" name="password"/>
                <input type="submit" />
            </form>
            {err&&<div>{err}</div>}
            <Link to='/forgot'>Hai dimenticato la password? Ripristinala</Link>
            <Link to='/get_verification_link'>Non ti è arrivato il link di verifica oppure è scaduto?</Link>
            <LoginWithGoogle/>
        </>
        )
}
export default Login