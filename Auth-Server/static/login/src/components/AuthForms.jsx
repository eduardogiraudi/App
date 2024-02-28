import {BrowserRouter as Router} from 'react-router-dom'
import { Route, Routes } from "react-router-dom";
import ChangePassword from "./ChangePassword";
import Forgot from "./Forgot";
import Login from "./Login";
import Register from "./Register";
import ActivateAccount from "./ActivateAccount";
import Response from './Response'
import GetVerificationLink from './GetVerificationLink';
function AuthForms(){
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
                        <Route path='/get_verification_link' element={<GetVerificationLink/>}/>
                        <Route path="/response" element={<Response/>}/>
                    </Routes>                
            </Router>
        </>
    )
}
export default AuthForms