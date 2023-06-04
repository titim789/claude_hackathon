import logo from './logo.svg';
import './App.css';
import FrontPage from "./components/FrontPage"
import { useState, useEffect } from 'react';
import { getCompanyInfo } from './api/api';
 
function App() {

  const [companyInfo, setCompanyInfo] = useState([])
  const [tempCompanyView, setTempCompanyView] = useState([])
  const [userSearch, setUserSearch] = useState("")

  useEffect(()=>{
    updateCompanyData()
  },[])

  useEffect(()=>{
    updateFilteredData()
  },[userSearch])
  
  function filterData(){
    //filter here
    const filData = companyInfo.filter((item) =>
      item.company.toLowerCase().includes(userSearch.toLowerCase()) ||
      item.ticker.toLowerCase().includes(userSearch.toLowerCase()))

    return filData
  };

  function updateFilteredData(){
    const filData = filterData()
    setTempCompanyView(filData)
  };

  function updateCompanyData(){
    getCompanyInfo()
    .then((response)=>{
      console.log(response)
      setCompanyInfo(response.data)
      setTempCompanyView(response.data)
      }
    )
  }


  return (
    <div className="App">
      <FrontPage data={tempCompanyView?tempCompanyView:companyInfo} setUserSearch={setUserSearch}/>
    </div>
  );
}

export default App;
