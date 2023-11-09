import React, { useState } from 'react';
import './AddPlots.css';

const AddPlots = ({ onClose }) => {
    const [plotNumber, setPlotNumber] = useState(0);

    const decreasePlotNumber = () => {
        if (plotNumber > 0) {
            setPlotNumber(plotNumber - 1);
        }
    };

    const increasePlotNumber = () => {
        setPlotNumber(plotNumber + 1);
    };

    const handleAddClick = () => {
        // Handle adding plots here
        console.log(`Adding ${plotNumber} plots.`);
        // You can perform your logic here for adding plots
        // For example, send an API request to add plots to the database
        onClose(); // Close the popup after adding plots
    };

    return (
        <div className="popup-container">
            <div className="popup">
                <div className="message">How many plots do you want to add?</div>
                <div className="number-container">
                    <button className="button_num" onClick={decreasePlotNumber}>-</button>
                    <div className="number">{plotNumber}</div>
                    <button className="button_num" onClick={increasePlotNumber}>+</button>
                </div>
                <div className="button-container">
                    <button className="button" onClick={handleAddClick}>Add</button>
                    <button className="button cancel-button" onClick={onClose}>Cancel</button>
                </div>
            </div>
        </div>
    );
};

export default AddPlots;
