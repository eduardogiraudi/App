import { useState } from 'react';
import {BrowserRouter as Router} from 'react-router-dom'
import { Route, Routes } from "react-router-dom";

function OtpForm(){
    return (
        <>
            <Router>
                    <Routes>
                        <Route path='/' element={<Form/>}/>
                        <Route path='*' element={'not found!'}/>
                    </Routes>                
            </Router>
        </>
    )
}
function Form(){
    const [numValue, setNumValue] = useState('')
    const handleChange = (e)=>{
        const data = e.target.value
        if(/^[0-9]*$/.test(data)){
            setNumValue(data)
        }
    }
    return  <form>
                <input type="text" maxLength={4} onChange={handleChange} value={numValue} placeholder='inserisci il codice OTP che ti è stato inviato'/>
                <input type="submit"/>
            </form>
}
export default OtpForm