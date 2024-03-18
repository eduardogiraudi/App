
import { resourceServer, authServer } from "./components/settings";
import Main from "./components/Main"

function App(){


        // quando ci si logga verifica se si è loggati
        // da verificare bene bene
        // deve farlo in ogni rotta protetta poi, renderla una funzione riutilizzabile in futuro

         if(getCookie('token')){
            fetch(`${resourceServer}/resource/profile`, {
                method:'POST',
                headers: {
                    authorization: 'Bearer ' + getCookie('token')
                }
            }).then(res=>{
                if(res.status===200){
                    window.location.href = resourceServer
                    // return res.json().then((data)=>{console.log(data)})
                }
            });
        } 
        if(getCookie('refresh_token')){
            fetch(`${authServer}/auth/refresh_token`, {
                method: 'POST',
                headers: {
                    authorization: 'Bearer ' + getCookie('refresh_token')
                }
            }).then(res => {
                if (res.status === 200) {
                    // return res.json().then((data)=>{console.log(data)})
                    window.location.href = resourceServer
                }
            });
        } 


    return (
    <>
        <Main/>
    </>
    )
}export default App

function getCookie(name) {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
        const [cookieName, cookieValue] = cookie.split('=');
        if (cookieName === name) {
            return cookieValue;
        }
    }
    return null;
}
