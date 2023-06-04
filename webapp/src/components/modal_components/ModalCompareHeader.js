import * as React from 'react';
import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import { TextField, Button, ListItem } from '@mui/material';
import './css/ModalCompareHeader.css';


const ModalCompareHeader = ({setCompareValue, setCompared, comparer}) => {

    const handleSearch = (event) => {
      const searchData = event.target.value
      setCompareValue(searchData)
    }

    function handleSubmit(event){
        event.preventDefault();
        const data = new FormData(event.currentTarget)
        console.log(data.get("input"))
        setCompareValue(data.get("input"))
        setCompared(true)
    }

    return(
        <div style={{display:"flex", flexDirection:"column", "alignItems":"center", }}>
        <h2>Compare To <u>{comparer}'s</u> Peers</h2>
        <Box component="form" onSubmit={handleSubmit} display="flex" sx={{justifyContent:"center"}} noValidate>
          <div className = "modalsearchbar">
            <TextField
                margin="normal"
                fullWidth
                id="input"
                name="input"
                placeholder='Enter Company Name/Ticker Code'
                onChange={handleSearch}
                sx={{padding:"5px"}}
                autoFocus
              />
            <Button
              type="submit"
              variant="contained"
              className='searchbutton'
              sx={{padding:"5px", height: "40px"}}
            >
              Compare
            </Button>
          </div>
        </Box>
        </div>
    )
}

export default ModalCompareHeader