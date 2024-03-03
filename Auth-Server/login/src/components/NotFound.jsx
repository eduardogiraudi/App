import { Link } from "react-router-dom"

function NotFound(){
    return (
            <>
                <div>
                    Pagina inesistente
                </div>
                <Link to={'/login'}>Torna al login</Link>
            </>
    )
}export default NotFound