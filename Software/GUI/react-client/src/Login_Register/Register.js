import React, { useState } from "react";
import hydroponics2 from "./hydroponics_img2.png";
import { Link, useNavigate } from "react-router-dom";
import "./login_index.css";

function Register() {
  const [firstName, setFirstName] = useState(null);
  const [lastName, setLastName] = useState(null);
  const [email, setEmail] = useState(null);
  const [password, setPassword] = useState(null);
  const [confirmPassword, setConfirmPassword] = useState(null);
  const [passwordsMatch, setPasswordsMatch] = useState(true); // New state to track password matching
  const [emailExists, setEmailExists] = useState(false); // New state to track existing email
  const navigate = useNavigate();

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
      setEmailExists(false); // Reset emailExists state when the user edits the email field
    }
    if (id === "password") {
      setPassword(value);
    }
    if (id === "confirmPassword") {
      setConfirmPassword(value);
    }
  };

  const handleSubmit = async () => {
    // Check if passwords match before proceeding
    if (password === confirmPassword) {
      try {
        // Passwords match, proceed with registration
        setPasswordsMatch(true);

        // Perform your registration logic here
        const response = await fetch("http://localhost:5000/api/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            firstName,
            lastName,
            email,
            password,
          }),
        });

        const data = await response.json();

        if (response.ok) {
          // Registration successful, navigate to the desired page
          navigate("/garden");
        } else if (data.error.includes("exists")) {
          // Email already exists, set emailExists state
          setEmailExists(true);
        } else {
          // Other registration error, handle as needed
          console.error("Registration error:", data.error);
        }
      } catch (error) {
        console.error("Error during registration:", error);
      }
    } else {
      // Passwords do not match, set state to indicate the mismatch
      setPasswordsMatch(false);
    }
  };

  return (
    <div style={{ backgroundColor: "#CFE1C9" }}>
      <div className="navBar"> </div>
      <div className="register">
        <div className={"loginMainContainer"}>
          <div className={"loginTitleContainer"}>
            <div>Register For</div>
          </div>
          <div className={"loginSubtitleContainer"}> GROWTH Web App</div>
          <div className="loginInputContainer">
            <label className="loginSubtitle2Container" htmlFor="firstName">
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

            <label className="loginSubtitle2Container" htmlFor="lastName">
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

            <label className="loginSubtitle2Container" htmlFor="email">
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
            {emailExists && (
              <div style={{ color: "red" }}>
                Email already exists. Please use a different email.
              </div>
            )}

            <label className="loginSubtitle2Container" htmlFor="password">
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

            <label
              className="loginSubtitle2Container"
              htmlFor="confirmPassword"
            >
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
            {!passwordsMatch && (
              <div style={{ color: "red" }}>
                Passwords do not match. Please try again.
              </div>
            )}
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
          <img src={hydroponics2} height={500} width={800} alt="Hydroponics" />
        </div>
      </div>
    </div>
  );
}

export default Register;
