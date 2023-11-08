import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import "./select_index.css";

const Select = ({ showModal, handleClose }) => {

  let firstScreen = false; 
  
  const modalStyle = {
    position: 'fixed',
    right: 0, // Adjust the right position as needed
    top: 0,
    bottom: 0,
    width: '400px', // Adjust the width as needed
    backgroundColor: 'white',
    zIndex: 1050,
    display: showModal ? 'block' : 'none',
  };
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (event) => {
    setSearchQuery(event.target.value);
    // Add code
  };

  const contentStyle = {
    flex: 1,
  };

  const footerStyle = {
    marginTop: 'auto',
  };

  return (
    <div>
    {firstScreen &&
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
    </div>}
    {!firstScreen && 
    <div style={modalStyle}>
          <div className="modal-content">
            <div className="modal-header">
              <button type="button" className="close" onClick={handleClose}>
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="modal-body" style={contentStyle}>
              <h5 className="subtitle3Container">Last Run Time:</h5>
              <p>Last Run Time: [Insert Time Here]</p>
              <table>
                <thead>
                  <tr>
                    <th>Temp</th>
                    <th>pH</th>
                    <th>Water Conductivity</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>[Temp Value]</td>
                    <td>[pH Value]</td>
                    <td>[Water Conductivity Value]</td>
                  </tr>
                </tbody>
              </table>
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
        </div>}
  </div>
    
   
  );
}
export default Select;



// //import FirstPopUp from "./FirstPopUp";
// import SecondPopUp from "./SecondPopUp";


// const Select = () => {
//   let firstScreen = true; 
//   return (

//     <div>
//       {firstScreen && <FirstPopUp/>}
//       {!firstScreen && <SecondPopUp/>}
//     </div>
   
//   );
// }
// export default Select;


