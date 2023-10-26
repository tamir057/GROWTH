import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import "./garden_index.css";

function Select({ showModal, handleClose }) {
  let firstScreen = true; 
  const modalStyle = {
    position: 'fixed',
    right: 0, // Adjust the right position as needed
    top: 0,
    bottom: 0,
    width: '300px', // Adjust the width as needed
    backgroundColor: 'white',
    zIndex: 1050,
    display: showModal ? 'block' : 'none',
  };
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (event) => {
    setSearchQuery(event.target.value);
    // You can add code here to perform the search based on the query.
  };

  const contentStyle = {
    flex: 1,
  };

  const footerStyle = {
    marginTop: 'auto',
  };

  return (
    <div style={modalStyle}>
      <div className="modal-content">
        <div className="modal-header">
          <button type="button" className="close" onClick={handleClose}>
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <h5 className="subtitle3Container">Select Plant:</h5>
        
        <div className="modal-body" style={contentStyle}>
          {/* Add a search bar input element */}
          <input
            type="text"
            placeholder="Search for plant..."
            value={searchQuery}
            onChange={handleSearch}
          />
          {/* Add your content for selecting options here */}
        </div>
        <div className={"subtitle2Container"}>  
        <Link to='/PlantProfile'> Create a New Plant Profile</Link> 
        </div>
        <div className="modal-footer" style={footerStyle}>
          <div className={"saveButton"}>
            <input
              className={"saveButton"}
              type="button"
              value={"Save"} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Select;
