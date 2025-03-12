import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { Button } from '@mui/material'
import Navbar from './Navbar'
import { StyledEngineProvider } from '@mui/material'


function App() {
  const [count, setCount] = useState(0)

  return (
    <StyledEngineProvider injectFirst>
      <Navbar />
    </StyledEngineProvider>
  )
}

export default App
