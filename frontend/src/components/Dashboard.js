import React from 'react';

const Dashboard = ({ data, prediction }) => {
  return (
    <div>
      <h2>Live Data</h2>
      <table>
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Open</th>
            <th>Close</th>
            <th>Prediction</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <tr key={index}>
              <td>{row.timestamp}</td>
              <td>{row.open}</td>
              <td>{row.close}</td>
              <td>{index === data.length - 1 ? prediction : ''}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Prediction: {prediction}</h2>
    </div>
  );
};

export default Dashboard;
