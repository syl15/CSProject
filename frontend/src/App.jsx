import { useState } from 'react'
import './App.css'
import TestAPI from "./TestAPI.jsx"
import Navbar from "./components/Navbar.jsx"
import Dashboard from "./Dashboard.jsx"

function App() {
  return (
    <>
      <TestAPI/>
      <Navbar/>
      <Dashboard/>
    </>
  )
}

export default App;
