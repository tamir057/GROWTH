import React from 'react';
import PropTypes from 'prop-types';
import './Garden.css'

const LoadingPopup = ({runType}) => {
  return (
    <>
    <div className="loading-popup">
        <div className="loading-content">
        <div className="loading-spinner"></div>
        <div className="loading-text">{runType}</div>
        </div>
    </div>
    </>
  );
};

LoadingPopup.propTypes = {
  isLoading: PropTypes.bool.isRequired,
};

export default LoadingPopup;