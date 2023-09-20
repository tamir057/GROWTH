import React, { useState, useEffect } from 'react'
import hydroponics2 from './hydroponics_img2.png'
import { Link } from 'react-router-dom';

function Register() {
    const [firstName, setFirstName] = useState(null);
    const [lastName, setLastName] = useState(null);
    const [email, setEmail] = useState(null);
    const [password,setPassword] = useState(null);
    const [confirmPassword,setConfirmPassword] = useState(null);

    const handleInputChange = (e) => {
        const {id , value} = e.target;
        if(id === "firstName"){
            setFirstName(value);
        }
        if(id === "lastName"){
            setLastName(value);
        }
        if(id === "email"){
            setEmail(value);
        }
        if(id === "password"){
            setPassword(value);
        }
        if(id === "confirmPassword"){
            setConfirmPassword(value);
        }

    }

    const handleSubmit  = () => {
        console.log(firstName,lastName,email,password,confirmPassword);
    }



return <div class='register'>
  
<div className="form-body">
<div className={"titleContainer"}>
      <div>Register For</div>
      </div>
      <div className={"subtitleContainer"}> GROWTH Web App</div>
        <div className="inputContainer">
            <label className="subtitle2Container" for="firstName">First Name </label>
            <input className="subtitle2Container" type="text" value={firstName} onChange = {(e) => handleInputChange(e)} id="firstName" placeholder="Enter your first name"/>
         <br />
            <label className="subtitle2Container" for="lastName">Last Name </label>
            <input  className="subtitle2Container" type="text" name="" id="lastName" value={lastName}  onChange = {(e) => handleInputChange(e)} placeholder="Enter your last name"/>
            <br />
            <label className="subtitle2Container" for="email">Email </label>
            <input className="subtitle2Container" type="email" id="email" value={email} onChange = {(e) => handleInputChange(e)} placeholder="Enter your email"/>
            <br />
            <label className="subtitle2Container" for="password">Password </label>
            <input className="subtitle2Container" type="password"  id="password" value={password} onChange = {(e) => handleInputChange(e)} placeholder="Enter a password"/>
            <br />
            <label className="subtitle2Container" for="confirmPassword">Confirm Password </label>
            <input className="subtitle2Container" type="password" id="confirmPassword" value={confirmPassword} onChange = {(e) => handleInputChange(e)} placeholder="Confirm password"/>
            <br />
      <input
          className={"inputButton"}
          type="button"
          onClick={handleSubmit}
          value={"Register"} />

        </div>
        <div className={"subtitle3Container"}> <p>Already Have an Account?  
        <Link to='/login'> Login</Link>  </p>
        </div>
    </div>
    <div><img  src={hydroponics2} height={500} width={800}  /></div>
  </div>


}
export default Register;
