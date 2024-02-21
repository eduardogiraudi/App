import { useEffect, useState } from "react"

function Register ({setErr, setSubmitBlock}){
    const [password, setPassword] = useState()
    const [confirmPassword, setConfirmPassword] = useState()
    const handlePasswordChange = (e) =>{
        setPassword(e.target.value)
    }
    const handleConfirmPasswordChange = (e) =>{
        setConfirmPassword(e.target.value)
    }
    // necessario useeffect o si prova a modificare lo stato prima del rendering causando errori
    useEffect(()=>{
        if(password && confirmPassword){
            if(password!==confirmPassword){
                setErr('Le password non coincidono')
                setSubmitBlock(true)
            }else if (password.length < 8 || !/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[-!@#$%^&*()_+`~={}[\]:;"'<>,.?\\/])[A-Za-z\d-!@#$%^&*()_+`~={}[\]:;"'<>,.?\\/]{8,}$/.test(password)) {
                setErr('La password deve contenere almeno 8 caratteri alfanumerici (almeno un numero, un simbolo, una lettera minuscola e una lettera maiuscola).');
                setSubmitBlock(true)
            }else{
                setSubmitBlock(false)
            }
        } 
        return ()=>setErr('')
    },[password, confirmPassword])
    return (
        <>
            <input type="text" name='username' placeholder="username"/>
            <input type="email" name="email" placeholder="email"/>
            <input type="password" name="password" onChange={handlePasswordChange} placeholder="password"/>
            <input type="password" name="confirm_password" onChange={handleConfirmPasswordChange} placeholder="confirm password"/>
        </>
    )
}export default Register