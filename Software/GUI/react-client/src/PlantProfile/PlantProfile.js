import React, { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import { AiOutlineSearch } from "react-icons/ai";
import "bootstrap/dist/css/bootstrap.css";
import "./PlantProfile.css";
import img from "./lettuce.png";

function PlantProfile() {
  //   const [plantName, setPlantName] = useState("");
  //   const [ph, setPH] = useState(0);
  //   const [ec, setEC] = useState(0);
  //   const [hoursLight, setHoursLight] = useState("");

  return (
    <div>
      <div className="navBar">Garden Profile</div>
      <div className={"mainContainer"}>
        <div className={"bodyContainer"}>
          <Container className={"leftPanel"}>
            <div className={"header"}>Create Plant Profile</div>
            <div className="row searchBar">
              <div className=" position-relative">
                <input
                  placeholder="Search Plant"
                  className="form-control rounded-pill ps-5"
                />
                <AiOutlineSearch
                  className="fs-3 position-absolute 
                       wd-nudge-up"
                />
              </div>
            </div>
            <div className={"plantField"}>
              <div className={"plantFieldTitle"}>Name:</div>
              <input placeholder="ex. Lettuce" className="plantFieldInput" />
            </div>
            <div className={"plantField"}>
              <div className={"plantFieldTitle"}>Ideal pH:</div>
              <input placeholder="ex. 5.0-6.0" className="plantFieldInput" />
            </div>
            <div className={"plantField"}>
              <div className={"plantFieldTitle"}>Ideal EC:</div>
              <input placeholder="ex. 0.8-1.2" className="plantFieldInput" />
            </div>
            <div className={"plantField"}>
              <div className={"plantFieldTitle"}>Ideal Hours of Light:</div>
              <input placeholder="ex. 10-12" className="plantFieldInput" />
            </div>
            <div className={"plantFieldTitle"}>Plot</div>
            <div className="plotContainer">
              <div className="plotRow"></div>
              <div className="plotRow"></div>
              <div className="plotRowEmpty"></div>
            </div>
          </Container>
          <div className={"rightPanel"}>
            <div className={"header"}>Lettuce Plant</div>
            <div className="imgContainer">
              <img src={img} alt="" />
            </div>
            <div className={"longPlantDescription"}>
              <p>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
                enim ad minim veniam, quis nostrud exercitation ullamco laboris
                nisi ut aliquip ex ea commodo consequat.
              </p>
              <p>
                Sed ut perspiciatis unde omnis iste natus error sit voluptatem
                accusantium doloremque laudantium, totam rem aperiam, eaque ipsa
                quae ab illo inventore veritatis et quasi architecto beatae
                vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia
                voluptas sit aspernatur aut odit aut fugit, sed quia
                consequuntur magni dolores eos qui ratione voluptatem sequi
                nesciunt.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
export default PlantProfile;
