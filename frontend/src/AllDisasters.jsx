import React from 'react'
import Navbar from './components/Navbar'
import DisasterCard from './components/DisasterCard'
import FilterColumn from './components/FilterColumn'
import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard'

const BASE_URL = "http://127.0.0.1:5001"; // Flask API URL
import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard'

const BASE_URL = "http://127.0.0.1:5001"; // Flask API URL

export default function AllDisasters() {
    const [disasters, setDisasters] = useState([]);
    const [currIndex, setCurrIndex] = useState(0);
    const navigate = useNavigate();

    // Fetch disasters on mount 
    useEffect(() => {
        // Add parameters if necessary
        fetch(`${BASE_URL}/disasters`) // Ex. /disasters?limit=1 
            .then((result) => result.json())
            .then(setDisasters)
            .catch(console.error);
    }, [])

    if(!disasters) {
      return <div>Loading...</div>
    }

    const navigateToDisaster = (disaster) => {
      navigate(`/AllDisasters/${disaster.name}`, { state: disaster });
    }

    const back = () => {
      if(currIndex > 0) {
        setCurrIndex(currIndex-3);
      }
    }

    const next = () => {
      if (currIndex < disasters.length - 1) {
        setCurrIndex(currIndex + 3);
      }
    };
    
    

    return (
      <div className="flex flex-col mt-30 min-w-screen min-h-screen h-auto absolute left-0 right-0 px-10 md:px-20 pb-10 overflow-x-hidden">
          <h1 className="text-4xl font-bold text-left">All Disasters</h1>
          <div className="flex flex-col gap-y-10 md:flex-row w-full">
              <FilterColumn/>
              
              <div className="flex flex-col w-full md:mt-15">
                {disasters.slice(currIndex,currIndex+3).map((disaster) => (
                  <div key={disaster.id} className="mb-5 rounded-md cursor-pointer max-w-xl hover:bg-gray-100" onClick={() => navigateToDisaster(disaster)}>
                      <DisasterCard disaster={disaster}/>
                  </div>
                  
                ))}
                <div className="flex flex-row gap-x-3 mt-3 relative">
                  <button onClick={back} className="border border-[#D4D4D4] rounded-md">Previous</button>
                  <button onClick={next} className="border border-[#D4D4D4] rounded-md">Next</button>
                </div>
              </div>
            
              
          </div>

          
      </div>
    )
          
      </div>
    )
}