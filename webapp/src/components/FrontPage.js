import Button from '@mui/material/Button';
import { useState } from 'react';
import CustomSearchBar from './CustomSearchBar';
import CustomTable from './CustomTable';
import Header from './Header';
import Footer from './Footer';
import APIButton from './api_button';

const FrontPage = ({temp, setTemp}) => {
    const [toggle, setToggle] = useState(false)

    const data = [
        { company: 'John', rating: 23, remarks: "Aye aye captain!" },
        { company: 'Mary', rating: 18, remarks: "Had a little lamb, it was white as snow!"},
        { company: 'Peter', rating: 45, remarks: "Pan and Tinklebell."}
      ];

    function handleClick() {
        setToggle(!toggle)
        console.log("EMAIL TO USER")
        if(toggle){
            setTemp("GIM AIK IS DA BESTTT")
        }
        else {
            setTemp("TITUS IS BETTERRR")
        }
    }

    return (
        <div>
            <Header/>
            <CustomSearchBar/>    
            <CustomTable columns={["company", "rating", "remarks"]} data={data}/>
            THIS IS THE {temp}
            <Button onClick={handleClick} variant="outlined">
            Click Me</Button>
            <APIButton/>
            <Footer/>
        </div>
    )
}

export default FrontPage