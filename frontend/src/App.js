import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Dashboard from './components/Dashboard';

const App = () => {
  const [prediction, setPrediction] = useState("");
  const [cryptoData, setCryptoData] = useState([]);

  useEffect(() => {
    const fetchData = () => {
      axios.get('http://localhost:5000/update_data')
        .then(response => {
          console.log("Data updated:", response.data);
        })
        .catch(error => console.log(error));

      axios.get('http://localhost:5000/predict')
        .then(response => {
          setPrediction(response.data.prediction);
        })
        .catch(error => console.log(error));
    };

    fetchData();
    const interval = setInterval(fetchData, 60000);  // Update every minute

    axios.get('http://localhost:5000/api/crypto_data')
      .then(response => {
        setCryptoData(response.data);
      })
      .catch(error => console.log(error));

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>Crypto Trading Dashboard</h1>
      <Dashboard data={cryptoData} prediction={prediction} />
    </div>
  );
}

export default App;
