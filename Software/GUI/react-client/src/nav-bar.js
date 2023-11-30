import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import "./Garden/Garden.css";

function NavBar() {
  const { pathname } = useLocation();
  const history = useNavigate();

  const handleLogout = async () => {
    try {
      const response = await axios.post("http://localhost:5000/api/logout");

      console.log("Logout response:", response.data);

      if (response.data.success) {
        // Clear any client-side user information or state
        // For simplicity, let's reload the page to clear all client-side state

        window.location.reload();
        history.push("/login");

      } else {
        console.error("Logout failed:", response.data.message);
      }
    } catch (error) {
      console.error("Logout error:", error.message);
    }
  };

  const [ignore, active] = pathname.split("/");

  return (
    <div className="w-100 pos-fixed bg-primary-green">
      <div className="row">
        <div className="white-text col-3 p-2 ml-10">
          <h3>GROWTH</h3>
        </div>
        <div className="col-9">
          <ul className="nav nav-pills mb-2 mt-2 float-end">
            <li className="nav-item">
              <Link
                to="/garden"
                className={`white-text nav-link ${active === "about" ? "active" : ""}`}
              >
                Garden
              </Link>
            </li>
            <li className="nav-item">
              <Link
                to="/plantprofile"
                className={`white-text nav-link ${active === "home" ? "active" : ""}`}
              >
                Profile
              </Link>
            </li>
            <li className="nav-item">
              <button className="btn white-text nav-link" onClick={() => { handleLogout(); }}>
                Log Out
              </button>
            </li>
          </ul>
        </div>
      </div>

    </div>
  );
}

export default NavBar;
