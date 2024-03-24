import { Link } from "react-router-dom"

function NotFound(){
    return (
            <>
                <div>
                    Pagina inesistente
                </div>
                <Link to={'/'}>Torna indietro</Link>
            </>
    )
}export default NotFound