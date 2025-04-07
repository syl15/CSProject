import { useState } from 'react'
import './App.css'
import TestAPI from "./TestAPI.jsx"
import Navbar from "./components/Navbar.jsx"
import { Route, Routes } from 'react-router-dom'
import AllDisasters from './AllDisasters.jsx'
import RecentDisaster from './RecentDisaster.jsx'
import Dashboard from './components/Dashboard.jsx'

function App() {
  return (
    <>
      <TestAPI/>
      <Navbar/>
      <div>
        <Routes>
          <Route path="/"  element={<RecentDisaster/>} />
          <Route path="/AllDisasters"  element={<AllDisasters/>} />
          <Route path="/AllDisasters/:disasterName" element={<Dashboard />} />
        </Routes>
        
      </div>
      
    </>
  )
}

export default App;
