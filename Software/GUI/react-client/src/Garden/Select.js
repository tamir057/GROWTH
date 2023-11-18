import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import "./select_index.css";
import axios from 'axios';


const Select = ({ showModal, handleClose, plotNumber }) => {
  const [emptyPlot, setEmptyPlot] = useState(true); // State for controlling the screen

  useEffect(() => {
    // Fetch the plot document based on plotNumber
    const fetchPlot = async () => {
      try {
        const response = await axios.get(`/api/plots/${plotNumber}`); // Replace with your actual endpoint
        const plot = response.data;

        // Update firstScreen based on whether the plant field is an empty string or not
        setEmptyPlot(plot.plant_id === "");
      } catch (error) {
        console.error('Error fetching plot:', error);
      }
    };

    // Call the fetchPlot function
    fetchPlot();
  }, [plotNumber]); // Add plotNumber to the dependency array

  const modalStyle = {
    position: 'fixed',
    right: 0, // Adjust the right position as needed
    top: 0,
    bottom: 0,
    width: '400px', // Adjust the width as needed
    backgroundColor: '#F7FCFC',
    zIndex: 1050,
    display: showModal ? 'block' : 'none',
    paddingLeft: '20px',
  };
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPlant, setSelectedPlant] = useState('');
  const [plantOptions, setPlantOptions] = useState([]);

  useEffect(() => {
    // Fetch plant options from your endpoint
    const fetchPlants = async () => {
      try {
        const response = await axios.get('/api/plants'); // Replace with your actual endpoint
        setPlantOptions(response.data);
      } catch (error) {
        console.error('Error fetching plant options:', error);
      }
    };

    // Call the fetchPlants function
    fetchPlants();
  }, []);

  const handleSave = async () => {
    try {
      // Make a POST request to your backend endpoint with plot number and selected plant
      const response = await axios.post(`/api/assign-plant`, {
        plotNumber: plotNumber,
        selectedPlant: selectedPlant,
      });

      // Handle the response as needed
      console.log('Plant assigned successfully:', response.data);

      // Close the modal or perform any other necessary actions
      handleClose();
      window.location.reload();
    } catch (error) {
      console.error('Error assigning plant to plot:', error);
      // Handle the error as needed
    }
  };
  const contentStyle = {
    flex: 1,
  };

  const footerStyle = {
    marginTop: 'auto',
  };
  return (
    <div>
    {emptyPlot &&
    <div style={modalStyle}>
      <div className="modal-content">
        <div className="modal-header">
          <button type="button" className="close" onClick={handleClose}>
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <h5 className="subtitle3Container">Select Plant:</h5>
        <div className="modal-body" style={contentStyle}>
            <select
              value={selectedPlant}
              onChange={(e) => setSelectedPlant(e.target.value)}
              className="custom-dropdown"
            >
              {/* Map through the fetched plant options and create options dynamically */}
              {plantOptions.map((plant) => (
                <option key={plant._id} value={plant.name}>
                  {plant.name}
                </option>
              ))}
            </select>
          </div>        
        <div className={"subtitle2Container"}>  
        <Link to='/PlantProfile'> Create a New Plant Profile</Link> 
        </div>
        <div className="modal-footer" style={footerStyle}>
          <div className={"saveButton"}>
          <input
            className={"saveButton"}
            type="button"
            value={"Save"}
            onClick={handleSave}
          />
          </div>
        </div>
      </div>
    </div>}
    {!emptyPlot && 
    <div style={modalStyle}>
          <div className="modal-content">
            <div className="modal-header">
              <button type="button" className="close" onClick={handleClose}>
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div className="modal-body" style={contentStyle}>
              <h5 className="runTimeContainer">Last Run Time:</h5>
              <p>[Insert Time Here]</p>
              <table>
                <tbody>
                  <tr>
                    <th>Temp: </th>
                    <td>[Temp Value]</td>
                  </tr>
                  <tr>
                    <th>pH: </th>
                    <td>[pH Value]</td>
                  </tr>
                  <tr>
                    <th>Water Conductivity: </th>
                    <td>[Water Conductivity Value]</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="modal-footer" style={footerStyle}>
              <div className = 'topPadding'>
              <div className={"saveButton"}>
                <input
                  className={"saveButton"}
                  type="button"
                  value={"Save"} />
              </div>
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


