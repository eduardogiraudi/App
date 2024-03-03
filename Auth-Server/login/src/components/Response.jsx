import { Link, useLocation } from "react-router-dom"

function Response(){
    let location = useLocation()
    const message = location.state?.message || 'C\'è stato un errore oppure la pagina non è stata aperta nella maniera corretta';
    return (
            <>
                <Link to={-1}>Torna indietro</Link>
                <div>{message}</div>
                <Link to={'/login'}>Login</Link>
            </>
            )
}export default Response