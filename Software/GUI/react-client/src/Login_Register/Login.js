import React, { useState, useEffect } from "react";
import hydroponics from "./hydroponics_img.png";
import hydroponics2 from "./hydroponics_img2.png";
import "./login_index.css";
import { Link } from "react-router-dom";
import { useNavigate } from 'react-router-dom';


function Login() {
  const [data, setData] = useState([{}]);
  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");
  const [password, setPassword] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [email, setEmail] = useState("");
  
  const navigate = useNavigate();

  useEffect(() => {
    fetch("/members")
      .then((res) => res.json())
      .then((data) => {
        setData(data);
        console.log(data);
      });
  }, []);

  const onButtonClick = () => {
    navigate('/garden');
  };

  return (
    <div style={{ backgroundColor: '#CFE1C9' }}>
    <div className = 'navBar'> </div>
    <div className="login">
       
      <div className={"loginMainContainer"}>
        <div className={"loginTitleContainer"}>
          <div>Login To</div>
        </div>
        <div className={"loginSubtitleContainer"}> GROWTH Web App</div>
        <br />
        <div className={"loginInputContainer"}>
          <div className={"loginSubtitle2Container"}> Email</div>
          <input
            value={email}
            placeholder="Enter your email here"
            onChange={(ev) => setEmail(ev.target.value)}
            className={"loginInputBox"}
          />
          <label className="errorLabel">{emailError}</label>
        </div>
        <br />
        <div className={"loginInputContainer"}>
          <div className={"loginSubtitle2Container"}> Password </div>
          <input
            type="password"
            value={password}
            placeholder="Enter your password here"
            onChange={(ev) => setPassword(ev.target.value)}
            className={"loginInputBox"}
          />
          <label className="errorLabel">{passwordError}</label>
        </div>
        <br />
        <div className={"loginInputContainer"}>
          <input
            className={"buttonLogin"}
            type="button"
            onClick={onButtonClick}
            value={"Log In"}
          />
        </div>
        <div className={"loginSubtitle3Container"}>
          {" "}
          <p>
            Don't Have an Account?
            <Link to="/register"> Register</Link>{" "}
          </p>
        </div>
      </div>
      <div>
        <img src={hydroponics2} height={500} width={800} />
      </div>
    </div>
    </div>
  );
}
export default Login;
