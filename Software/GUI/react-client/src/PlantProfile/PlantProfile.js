import React, { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import { AiOutlineSearch } from "react-icons/ai";
import "bootstrap/dist/css/bootstrap.css";
import "./PlantProfile.css";
import img from "./lettuce.png";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function PlantProfile() {
  const navigate = useNavigate();
  const initPlantRecs = {
    plant1: {
      plantName: "",
      plantDesc: "",
    },
    plant2: {
      plantName: "",
      plantDesc: "",
    },
    plant3: {
      plantName: "",
      plantDesc: "",
    },
  };

  const [searchField, setSearchField] = useState("");
  const [plantName, setPlantName] = useState("");
  const [minPH, setMinPH] = useState(0);
  const [maxPH, setMaxPH] = useState(0);
  const [minEC, setMinEC] = useState(0);
  const [maxEC, setMaxEC] = useState(0);
  const [minTemp, setMinTemp] = useState(0);
  const [maxTemp, setMaxTemp] = useState(0);
  const [minHoursLight, setMinHoursLight] = useState(0);
  const [maxHoursLight, setMaxHoursLight] = useState(0);
  const [plantDesc, setPlantDesc] = useState("");
  const [plantRecs, setPlantRecs] = useState(initPlantRecs);
  const [showRecs, setShowRecs] = useState(true);

  const openaiApiKey = "{insert OpenAI API key}";

  useEffect(() => {
    const fetchPlantRecs = async () => {
      try {
        await generatePlantRecs();
      } catch (error) {
        console.error("Error generating plant recs on page enter:", error);
      }
    };

    fetchPlantRecs();
  }, []);

  const handleSavePlant = () => {
    const plantInfo = {
      name: plantName,
      min_pH: minPH,
      max_pH: maxPH,
      min_ec: minEC,
      max_ec: maxEC,
      min_temp: minTemp,
      max_temp: maxTemp,
      min_hours_light: minHoursLight,
      max_hours_light: maxHoursLight,
      description: plantDesc,
    };
    // Make a POST request to save plant profile in the db
    fetch("http://10.110.203.52:5000/api/save-plant-profile", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(plantInfo),
    })
      .then((response) => response.json())
      .catch((error) =>
        console.error("Error saving new plant profile:", error)
      );
    navigate("/garden");
  };

  const getPlantNames = async () => {
    const responsePlants = await axios.get(
      "http://10.110.203.52:5000/api/plants"
    ); // Replace with your actual endpoint
    const plantNames = responsePlants.data.map((plant) => plant.name);
    return plantNames;
  };

  const callOpenAIForPlantRec = async () => {
    try {
      const plantNames = await getPlantNames();
      const plantNamesString = plantNames.join(", ");
      console.log("plant names in db: ", plantNamesString);
      const response = await axios.post(
        `https://api.openai.com/v1/chat/completions`,
        {
          model: "gpt-3.5-turbo",
          messages: [
            {
              role: "user",
              content: `given this list of plants: ${plantNamesString}, please generate three plants that grow well hydroponically that are NOT in the given list. Make sure the new plants are not in the given list. Please return only a JSON object with fields {"plant1": {"plantName", "plantDesc"}, "plant2": {"plantName", "plantDesc"}, "plant3": {"plantName", "plantDesc"}, }`,
            },
          ],
          max_tokens: 200,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${openaiApiKey}`,
          },
        }
      );
      console.log("OpenAI plant recommendations response:", response.data);
      const generatedPlantRecs = response.data.choices[0]?.message?.content;
      return generatedPlantRecs;
    } catch (error) {
      console.error(
        "Error calling OpenAI endpoint to get plant recommendations:",
        error
      );
      throw error;
    }
  };

  const callOpenAIForPlantInfo = async (plantName) => {
    try {
      const response = await axios.post(
        `https://api.openai.com/v1/chat/completions`,
        {
          model: "gpt-3.5-turbo",
          messages: [
            {
              role: "user",
              content: `what is the ideal ph, ideal electrical conductivity, ideal temperature, and ideal temperature of water and ideal hours of light for ${plantName} to grow in hydroponically. please give the answer as a json object with min ph, max ph, (where the max difference is 0.7), min electrical conductivity, max electrical conductivity  (where the is max difference between min and max ec is 0.7), min temperature, max temperature (in Celcius with a maximum range of 5 degrees), and min hours of light, max hours of light? Please also include a short description about growing ${plantName} hydroponically and how long it typically takes for the plant to grow. Please only respond with a json object  with fields "pH_min", "pH_max", "ec_min", "ec_max", "temp_min", "temp_max", "hours_light_min", "hours_light_max", "description" and do not elaborate. Please do not include the max range of values in the description`,
            },
          ],
          max_tokens: 400,
        },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${openaiApiKey}`,
          },
        }
      );
      console.log("OpenAI plant info response:", response.data);
      const plantInfo = response.data.choices[0]?.message?.content;
      return plantInfo;
    } catch (error) {
      console.error("Error calling OpenAI endpoint to get plantInfo:", error);
      throw error;
    }
  };

  const generatePlantRecs = async () => {
    try {
      //TODO: call to get the existing plants
      const response = await callOpenAIForPlantRec();
      const plantRecs = JSON.parse(response);
      setPlantRecs(plantRecs);
    } catch (error) {
      console.error("Error generating plant info:", error);
    }
  };

  const generatePlantInfo = async (newPlantName) => {
    setShowRecs(false);
    try {
      const response = await callOpenAIForPlantInfo(newPlantName);
      const plantInfo = JSON.parse(response);
      const capitalizedPlantName =
        newPlantName.charAt(0).toUpperCase() + newPlantName.slice(1);
      setPlantName(capitalizedPlantName);
      setMinPH(plantInfo.pH_min);
      setMaxPH(plantInfo.pH_max);
      setMinEC(plantInfo.ec_min);
      setMaxEC(plantInfo.ec_max);
      setMinTemp(plantInfo.temp_min);
      setMaxTemp(plantInfo.temp_max);
      setMinHoursLight(plantInfo.hours_light_min);
      setMaxHoursLight(plantInfo.hours_light_max);
      setPlantDesc(plantInfo.description);
      console.log(plantInfo.description);
    } catch (error) {
      console.error("Error generating plant info:", error);
    }
  };

  return (
    <div>
      <div className="navBar">Garden Profile</div>
      <div className={"mainContainer"}>
        <div className={"bodyContainer"}>
          <Container className={"leftPanel"}>
            <div className={"header"}>Create Plant Profile</div>

            <div className="row searchBar">
              <div className="col-md-9">
                <div className=" position-relative">
                  <input
                    placeholder="Search Plant"
                    className="form-control rounded-pill ps-5"
                    value={searchField}
                    onChange={(e) => setSearchField(e.target.value)}
                  />

                  <AiOutlineSearch
                    className="fs-3 position-absolute 
                       wd-nudge-up"
                  />
                </div>
              </div>
              <div className="col-md-3">
                <button
                  className="m-2 btn button-primary-2 round-15 float-end searchFieldButton"
                  onClick={async () => await generatePlantInfo(searchField)}
                >
                  search
                </button>
              </div>
            </div>

            <div className={"plantField"}>
              <div className={"plantFieldTitle"}>Name:</div>
              <input
                placeholder="ex. Lettuce"
                className="plantFieldInput"
                value={plantName || ""}
                onChange={(e) => setPlantName(e.target.value)}
              />
            </div>
            <div className={"plantField"}>
              <div className={"plantFieldTitle"}>Ideal pH:</div>
              <div className={"plantFieldsInputNumbersContainer"}>
                <input
                  placeholder="ex. 5.0"
                  className="plantFieldInput plantFieldInputNumber"
                  value={minPH || ""}
                  onChange={(e) => setMinPH(e.target.value)}
                />
                -
                <input
                  placeholder="ex. 6.0"
                  className="plantFieldInput plantFieldInputNumber"
                  value={maxPH || ""}
                  onChange={(e) => setMaxPH(e.target.value)}
                />
              </div>
            </div>
            <div className={"plantField"}>
              <div className={"plantFieldTitle"}>Ideal EC (mS/cm):</div>
              <div className={"plantFieldsInputNumbersContainer"}>
                <input
                  placeholder="ex. 1.3"
                  className="plantFieldInput plantFieldInputNumber"
                  value={minEC || ""}
                  onChange={(e) => setMinEC(e.target.value)}
                />
                -
                <input
                  placeholder="ex. 1.8"
                  className="plantFieldInput plantFieldInputNumber"
                  value={maxEC || ""}
                  onChange={(e) => setMaxEC(e.target.value)}
                />
              </div>
            </div>
            <div className={"plantField"}>
              <div className={"plantFieldTitle"}>Ideal Temperature (C):</div>
              <div className={"plantFieldsInputNumbersContainer"}>
                <input
                  placeholder="ex. 65"
                  className="plantFieldInput plantFieldInputNumber"
                  value={minTemp || ""}
                  onChange={(e) => setMinTemp(e.target.value)}
                />
                -
                <input
                  placeholder="ex. 75"
                  className="plantFieldInput plantFieldInputNumber"
                  value={maxTemp || ""}
                  onChange={(e) => setMaxTemp(e.target.value)}
                />
              </div>
            </div>
            <div className={"plantField"}>
              <div className={"plantFieldTitle"}>Ideal Hours of Light:</div>
              <div className={"plantFieldsInputNumbersContainer"}>
                <input
                  placeholder="ex. 14"
                  className="plantFieldInput plantFieldInputNumber"
                  value={minHoursLight || ""}
                  onChange={(e) => setMinHoursLight(e.target.value)}
                />
                -
                <input
                  placeholder="ex. 16"
                  className="plantFieldInput plantFieldInputNumber"
                  value={maxHoursLight || ""}
                  onChange={(e) => setMaxHoursLight(e.target.value)}
                />
              </div>
            </div>
            <button
              className="m-2 btn button-primary-2 round-15 float-center"
              onClick={handleSavePlant}
            >
              Save
            </button>
          </Container>
          {showRecs && (
            <div className={"rightPanel"}>
              <div className="header">Plant Recommendations</div>
              <div></div>

              {Object.keys(plantRecs).map((plantKey) => (
                <div
                  className="plantRecContainer"
                  key={plantKey}
                  onClick={async () => {
                    const newPlantName = plantRecs[plantKey].plantName;
                    console.log(newPlantName);
                    const capitalizedPlantName =
                      newPlantName.charAt(0).toUpperCase() +
                      newPlantName.slice(1);
                    setPlantName(capitalizedPlantName);
                    await generatePlantInfo(capitalizedPlantName);
                  }}
                >
                  <p className="plantRecName">
                    {plantRecs[plantKey].plantName}
                  </p>
                  <p>{plantRecs[plantKey].plantDesc}</p>
                </div>
              ))}
            </div>
          )}
          {!showRecs && (
            <div className={"rightPanel"}>
              <div className={"header"}>{plantName} Plant</div>
              <div className="imgContainer">
                <img src={img} alt="" />
              </div>
              <div className={"longPlantDescription"}>
                <p>{plantDesc}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
export default PlantProfile;
