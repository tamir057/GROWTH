import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

const GraphComponent = () => {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('your_backend_api_endpoint');
        const fetchedData = response.data;

        // Process your data if needed
        // For example, convert time strings to Date objects
        const processedData = fetchedData.map(entry => ({
          ...entry,
          time: new Date(entry.time),
        }));

        setData(processedData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  const chartData = {
    labels: data.map(entry => entry.time.toISOString()), // Use time as labels
    datasets: [
      {
        label: 'pH',
        data: data.map(entry => entry.pH),
        borderColor: 'red',
        fill: false,
      },
      // Add more datasets for other properties like temperature and ec
    ],
  };

  return <Line data={chartData} />;
};

export default GraphComponent;