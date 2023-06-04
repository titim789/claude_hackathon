import React from 'react';
import axios from 'axios';

function APIButton() {
  const fetchData = () => {
    axios.get('http://localhost:5000/api/getCompanyInfo')
      .then(response => {
        console.log(response.data);
        // Process the received JSON data here
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  };

  return (
    <div>
      <button onClick={fetchData}>Fetch Data</button>
    </div>
  );
}

export default APIButton;