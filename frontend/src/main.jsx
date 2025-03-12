import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './App.css'
import Navbar from './Navbar.jsx'
import Dashboard from './Dashboard.jsx'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(

  <StrictMode>
    <App />
  </StrictMode>
)
