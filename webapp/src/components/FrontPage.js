import Button from '@mui/material/Button';
import { useState } from 'react';
import CustomSearchBar from './CustomSearchBar';

const FrontPage = ({temp, setTemp}) => {
    const [toggle, setToggle] = useState(false)

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
        </div>
    )
}

export default FrontPage