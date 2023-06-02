import * as React from 'react';
import { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import { TextField, Button } from '@mui/material';
import './CustomSearchBar.css';


const SearchBar = () => {
    const [input, setInput] = useState();

    useEffect(()=>{
        console.log(input)
    },[input])

    const handleSearch = (event) => {
      setInput(event.target.value)
    }

    function handleSubmit(event){
        event.preventDefault();
        const data = new FormData(event.currentTarget)
        console.log(data.get("input"))
    }

    return(
        <Box component="form" onSubmit={handleSubmit} display="flex" sx={{justifyContent:"center"}} noValidate>
          <div className = "searchbar">
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
              Search
            </Button>
          </div>
        </Box>
    )
}

export default SearchBar