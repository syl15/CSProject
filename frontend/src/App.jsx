import { useState } from 'react'
import './App.css'
import TestAPI from "./TestAPI.jsx"
import Navbar from './Navbar'
import Dashboard from './Dashboard.jsx'

function App() {
  return (
    <>
      <Navbar/>
      <Dashboard/>
      <TestAPI/>
    </>   
  );
}

export default App;
