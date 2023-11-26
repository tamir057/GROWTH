import React, { useState } from "react";
import hydroponics2 from "./hydroponics_img2.png";
import "./login_index.css";
import { Link } from "react-router-dom";
import { useNavigate } from 'react-router-dom';

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const onButtonClick = async () => {
    try {
      // Basic client-side validation
      if (!email || !password) {
        setError("Email and password are required");
        return;
      }

      // Make a POST request to login the user
      const response = await fetch("http://localhost:5000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: email,
          password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Login successful, navigate to the garden page
        navigate('/garden');
      } else {
        // Login unsuccessful, set error message
        setError(data.error || "Invalid username or password");
      }
    } catch (error) {
      setError("An unexpected error occurred");
    }
  };

  return (
    <div style={{ backgroundColor: '#CFE1C9' }}>
      <div className='navBar'> </div>
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
          {error && (
            <div className={"loginErrorContainer"}>
              <p>{error}</p>
            </div>
          )}
          <div className={"loginSubtitle3Container"}>
            {" "}
            <p>
              Don't Have an Account?
              <Link to="/register"> Register</Link>{" "}
            </p>
          </div>
        </div>
        <div>
          <img src={hydroponics2} height={500} width={800} alt="Hydroponics" />
        </div>
      </div>
    </div>
  );
}

export default Login;
