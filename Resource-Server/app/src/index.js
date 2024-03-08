import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';
import './css/index.css';
import axios from 'axios'
import { authServer, resourceServer } from './settings';


const root = ReactDOM.createRoot(document.getElementById('root'));
 

const getCookie = (name) => {
  const cookies = document.cookie.split(';');
  for (let cookie of cookies) {
    const [cookieName, cookieValue] = cookie.trim().split('=');
    if (cookieName === name) {
      return cookieValue;
    }
  }
  return null;
};
function setCookie (name, value)  {
  document.cookie = `${name}=${value}`;
};

root.render(

    <App/>

);

function App(){
  const [person, setPerson] = useState()

  const api = axios.create({
    baseURL: resourceServer,
  })
  const refreshApi = axios.create({
    baseURL: authServer,
  })
  api.interceptors.request.use(
    (config) => {
      const token = getCookie('token'); 
      if(token) config.headers.Authorization = `Bearer ${token}`;
      return config;
    },
    (error) => Promise.reject(error)
  )
  api.interceptors.response.use(
    (config) => config,
    async (error) => {
      if(error.response.status === 401){
        const refreshToken = getCookie('refresh_token')
        if (!refreshToken) {
          window.location.href = authServer
          console.log('bloccato riga 54');
          return Promise.reject(error)
        }
        try{
          const response = await refreshApi.post('/auth/refresh_token',{} ,{
            headers: {
              'Authorization': `Bearer ${refreshToken}`,
            }
          })
          const newToken = response.data.message; 
          setCookie('token',newToken)
          return api.request(error.config)
        }catch(err){
          window.location.href = authServer
          console.log('bloccato riga 68', err);
          return Promise.reject(err)
        }
      }
    }
  )
  api.post('/resource/profile').then(res=>setPerson(res.data.message))


  return `${person}`
}