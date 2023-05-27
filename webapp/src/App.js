import logo from './logo.svg';
import './App.css';
import FrontPage from "./components/FrontPage"
import { useState } from 'react';
 
function App() {
  const [temp, setTemp] = useState("BUTTON: ");


  return (
    <div className="App">
      <FrontPage temp={temp} setTemp={setTemp}/>
    </div>
  );
}

export default App;
