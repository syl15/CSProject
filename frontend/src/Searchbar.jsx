import React from 'react'
import { InputAdornment, TextField } from '@mui/material'
import SearchIcon from '@mui/icons-material/Search';

export default function Searchbar({paddingLeft}) {
  return (
    <TextField id="outlined-basic"
        sx={{
            pl:paddingLeft
        }}
        InputProps={{ 
            startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon/>
                </InputAdornment>
               ),
            sx: { height: "5.7vh", borderColor: '#D4D4D4'} 
        }}
        InputLabelProps={{ sx: { fontSize: "2vh", top: "-0.8vh"}}}
    />
    

  )
}
