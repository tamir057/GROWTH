import React from "react";
import { Link, useLocation } from "react-router-dom";
import "./Garden/Garden.css"

function NavBar() {
  const { pathname } = useLocation();
  const [ignore, active] = pathname.split("/");
  return (
    <div className="w-100 pos-fixed bg-primary-green">
      <div className="row"> 
      <div className="col-3 p-2 ml-10">
        <h3>|        GROWTH robot</h3>
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
        </ul>
      </div>
      </div>
    </div>
  );
}

export default NavBar;
