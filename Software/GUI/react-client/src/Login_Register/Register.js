import React, { useState, useEffect } from "react";
import hydroponics2 from "./hydroponics_img2.png";
import { Link } from "react-router-dom";
import "./login_index.css";

function Register() {
  const [firstName, setFirstName] = useState(null);
  const [lastName, setLastName] = useState(null);
  const [email, setEmail] = useState(null);
  const [password, setPassword] = useState(null);
  const [confirmPassword, setConfirmPassword] = useState(null);

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    if (id === "firstName") {
      setFirstName(value);
    }
    if (id === "lastName") {
      setLastName(value);
    }
    if (id === "email") {
      setEmail(value);
    }
    if (id === "password") {
      setPassword(value);
    }
    if (id === "confirmPassword") {
      setConfirmPassword(value);
    }
  };

  const handleSubmit = () => {
    console.log(firstName, lastName, email, password, confirmPassword);
  };

  return (
    <div style={{ backgroundColor: '#CFE1C9' }}>
    <div className = 'navBar'> </div>
    <div className="register">
    <div className={"loginMainContainer"}>
        <div className={"loginTitleContainer"}>
          <div>Register For</div>
        </div>
        <div className={"loginSubtitleContainer"}> GROWTH Web App</div>
        <div className="loginInputContainer">
          <label className="loginSubtitle2Container" for="firstName">
            First Name{" "}
          </label>
          <input
            className="loginInputBox"
            type="text"
            value={firstName}
            onChange={(e) => handleInputChange(e)}
            id="firstName"
            placeholder="Enter your first name"
          />

          <label className="loginSubtitle2Container" for="lastName">
            Last Name{" "}
          </label>
          <input
            className="loginInputBox"
            type="text"
            name=""
            id="lastName"
            value={lastName}
            onChange={(e) => handleInputChange(e)}
            placeholder="Enter your last name"
          />

          <label className="loginSubtitle2Container" for="email">
            Email{" "}
          </label>
          <input
            className="loginInputBox"
            type="email"
            id="email"
            value={email}
            onChange={(e) => handleInputChange(e)}
            placeholder="Enter your email"
          />

          <label className="loginSubtitle2Container" for="password">
            Password{" "}
          </label>
          <input
            className="loginInputBox"
            type="password"
            id="password"
            value={password}
            onChange={(e) => handleInputChange(e)}
            placeholder="Enter a password"
          />

          <label className="loginSubtitle2Container" for="confirmPassword">
            Confirm Password{" "}
          </label>
          <input
            className="loginInputBox"
            type="password"
            id="confirmPassword"
            value={confirmPassword}
            onChange={(e) => handleInputChange(e)}
            placeholder="Confirm password"
          />
          <br />
          <input
            className={"buttonLogin"}
            type="button"
            onClick={handleSubmit}
            value={"Register"}
          />
          <div className={"loginSubtitle3Container"}>
            {" "}
            <p>
              Already Have an Account?
              <Link to="/login"> Login</Link>{" "}
            </p>
          </div>
        </div>
      </div>
      <div>
        <img src={hydroponics2} height={500} width={800} />
      </div>
    </div>
    </div>
  );
}
export default Register;
