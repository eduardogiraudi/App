import { useState } from "react"
import {BrowserRouter as Router, useLocation} from 'react-router-dom'
import { Route, Routes, Link } from "react-router-dom";
import ChangePassword from "./ChangePassword";
import Forgot from "./Forgot";
import Login from "./Login";
import Register from "./Register";

import ActivateAccount from "./ActivateAccount";

function AuthForms(){
    const [loginRegisterForgot, setLoginRegisterForgot] = useState('login') 
    return (
        <>
            <Router>
                    <Routes>
                        <Route path="/" element={<Login/>}/>
                        <Route path="/login" element={<Login/>}/>
                        <Route path="/register" element={<Register/>}/>
                        <Route path="/forgot" element={<Forgot/>}/>
                        <Route path="/change_password" element={<ChangePassword/>}/>
                        <Route path="/activate_account" element={<ActivateAccount/>}/>
                        <Route path="/test" element="dio porcooooo"/>
                    </Routes>                
            </Router>
        </>
    )
}
export default AuthForms