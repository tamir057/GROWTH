import './AddPlots.css';

const WarningPopUp = ({ onClose }) => {

    return (
        <div className="popup-container">
            <div className="popup-warning center">
                <div className="message mt-4">Please select the plots you want to run.</div>
                <div className="button-container">
                    <button className="button" onClick={onClose}>OK</button>
                </div>
            </div>
        </div>  
    );
};

export default WarningPopUp;
