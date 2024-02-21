import { useLocation } from "react-router-dom";
import authServer from "./settings";
// far gestire a flask l'authorization header, è più sicuro così
function ChangePassword (){
    const location = useLocation();
    const queryParameters = new URLSearchParams(location.search);
    const handleChangePassword = (e)=>{
        e.preventDefault(); 
        const body = new FormData(e.currentTarget)
        const token = queryParameters.get('token');
        const url = authServer + '/auth/reset_password'
        console.log(token);
    }
    return (
        <>
            <form onSubmit={handleChangePassword}>
                <input type="password" name="password" placeholder="password"/>
                <input type="new_password" name="new_password" placeholder="new password"/>
                <input type="submit"/>
            </form>
        </>
    )
}
export default ChangePassword