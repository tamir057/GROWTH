import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import "./select_index.css";

function PlantInfo({ showModal, handleClose,plantName, temperature, pH, conductivity }) {
  //   const modalStyle = {
  //   position: 'fixed',
  //   right: 0, // Adjust the right position as needed
  //   top: 0,
  //   bottom: 0,
  //   width: '300px', // Adjust the width as needed
  //   backgroundColor: 'white',
  //   zIndex: 1050,
  //   display: showModal ? 'block' : 'none',
  // };

  // const footerStyle = {
  //   marginTop: 'auto',
  // };

  return (
    <div className="plant-info-container">
      <div className="plant-image">
        {/* Include plant image here */}
        <img src="plant_image.jpg" alt="Plant" />
      </div>
      <div className="plant-details">
        <h3>{plantName}</h3>
        <table>
          <tbody>
            <tr>
              <td>Temperature:</td>
              <td>{temperature} °C</td>
            </tr>
            <tr>
              <td>pH:</td>
              <td>{pH}</td>
            </tr>
            <tr>
              <td>Conductivity:</td>
              <td>{conductivity}</td>
            </tr>
          </tbody>
        </table>
        <button className="edit-button">
          Edit Plant Profile
        </button>
      </div>
    </div>
  );
}

export default PlantInfo;