import React from 'react';
import axios from 'axios';

function MyComponent() {
  const fetchData = () => {
    axios.get('/api/data')
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

export default MyComponent;