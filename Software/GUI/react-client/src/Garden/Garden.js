import React from "react";
import welcomeImage from "../images/welcome-banner.png";
import travelBunch from "../images/welcome-pack.png";
import "../css/index.css";

function Garden() {
  return (
    <div className="nav-padding position-relative mb-2 bg-my-primary wide">
      <div className="w-100">
        <img src={welcomeImage} className="w-100" alt={"Welcome"} />
        <br />
        <br />
        <br />
        <br />
        <br />
        <br />
      </div>
      <div className="row">
        <div className="col-sm-12 col-md-5 parent">
          <div className="center padding-70">
            <h1>Wander</h1>
            <h3>Travel with an Impact</h3>
            <p>
              Help small business build a name while vacationing around the world and exploring new adventures that await you!
            </p>
            <button
              onClick={handleClick}
              className="rounded-pill btn btn-primary"
            >
              Get Started
            </button>
          </div>
        </div>
        <div className="col-md-5 d-s-none">
        <img
              className="size-100"
              src={travelBunch}
              alt={"Tarvel 1"}
            />
        </div>
      </div>
    </div>
  );
}
export default Garden;
