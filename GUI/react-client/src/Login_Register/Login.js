import React, { useState, useEffect } from 'react'
import hydroponics from './hydroponics_img.png'
import hydroponics2 from './hydroponics_img2.png'
import { Link } from 'react-router-dom';

function Login() {
  const [data, setData] = useState([{}])    
  const [emailError, setEmailError] = useState("")
  const [passwordError, setPasswordError] = useState("")
  const [password, setPassword] = useState("")
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

const onButtonClick = () => {
  // update this function later
}

return <div class='login'>
<div className={"mainContainer"}>
  <div className={"titleContainer"}>
      <div>Login To</div>
      </div>
      <div className={"subtitleContainer"}> GROWTH Web App</div>
  <br />
  <div className={"inputContainer"}>
  <div className={"subtitle2Container"}> Email</div>
      <input
          value={email}
          placeholder="Enter your email here"
          onChange={ev => setEmail(ev.target.value)}
          className={"inputBox"} />
      <label className="errorLabel">{emailError}</label>
  </div>
  <br />
  <div className={"inputContainer"}>
  <div className={"subtitle2Container"}> Password </div>
      <input
          value={password}
          placeholder="Enter your password here"
          onChange={ev => setPassword(ev.target.value)}
          className={"inputBox"} />
      <label className="errorLabel">{passwordError}</label>
  </div>
  <br />
  <div className={"inputContainer"}>
      <input
          className={"inputButton"}
          type="button"
          onClick={onButtonClick}
          value={"Log In"} />
  </div>
  <div className={"subtitle3Container"}> <p>Don't Have an Account?  
  <Link to='/register'> Register</Link>  </p>
  </div>
  </div>
  <div><img src={hydroponics2} height={500} width={800}  /></div>
  </div>


}
export default Login;
