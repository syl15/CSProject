import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './App.css'
import Navbar from './Navbar.jsx'
import App from './App.jsx'
import MobileNavbar from './MobileNavbar.jsx'

createRoot(document.getElementById('root')).render(

  <StrictMode>

    <Navbar/>
  </StrictMode>
)
