import React from "react";
import { Link, useLocation } from "react-router-dom";
// import { useSelector } from "react-redux";
// import "./Garden/index.css"

function NavBar() {
//   const { currentUser } = useSelector((state) => state.user);
  const { pathname } = useLocation();
  const [ignore, active] = pathname.split("/");
  return (
    <div className="w-100 pos-fixed bg-primary-green">
      <ul className="nav nav-pills mb-2 mt-2 float-end">
        <li className="nav-item">
          <Link
            to="/garden"
            className={`nav-link ${active === "about" ? "active" : ""}`}
          >
            Garden
          </Link>
        </li>
        <li className="nav-item">
          <Link
            to="/profile"
            className={`nav-link ${active === "home" ? "active" : ""}`}
          >
            Profile
          </Link>
        </li>
      </ul>
    </div>
  );
}

export default NavBar;
