import React, { useState, useEffect } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import NavBar from "./nav-bar";
import { HashRouter, Navigate } from "react-router-dom";
import Login from './Login_Register/Login';
import Register from './Login_Register/Register';
import Garden from './Garden/Garden';
import PlantProfile from './PlantProfile/PlantProfile';

function App() {
  const [data, setData] = useState([{}])
  const [loggedIn, setLoggedIn] = useState(false)
  const [email, setEmail] = useState("")
  useEffect(() => {
    fetch("/members").then(
      res => res.json()
      
  ).then(
    data => {
      setData(data)
      console.log(data)
    }
  )
}, [])
return (
  <div>
  <HashRouter>
        <div>
        <NavBar />
          <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register/>} />
            <Route path="/garden" element={<Garden/>} />
            <Route path="/plantprofile" element={<PlantProfile/>} />
          </Routes>
        </div> 
      </HashRouter>
  </div>
);
}
export default App;
