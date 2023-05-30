import Button from '@mui/material/Button';
import { useState } from 'react';
import CustomSearchBar from './CustomSearchBar';
import CustomTable from './CustomTable';

const FrontPage = ({temp, setTemp}) => {
    const [toggle, setToggle] = useState(false)

    const data = [
        { name: 'John', age: 23 },
        { name: 'Mary', age: 18 },
        { name: 'Peter', age: 45 }
      ];

    function handleClick() {
        setToggle(!toggle)
        if(toggle){
            setTemp("GIM AIK IS DA BESTTT")
        }
        else {
            setTemp("TITUS IS BETTERRR")
        }
    }

    return (
        <div>
            <CustomSearchBar/>    
            THIS IS THE {temp}
            <Button onClick={handleClick} variant="outlined">
            CLICK ME</Button>
            <CustomTable columns={["name", "age"]} data={data}/>
        </div>
    )
}

export default FrontPage