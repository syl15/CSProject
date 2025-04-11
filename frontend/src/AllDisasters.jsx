import React from 'react'
import Navbar from './components/Navbar'
import DisasterCard from './components/DisasterCard'
import FilterColumn from './components/FilterColumn'
import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard'

export default function AllDisasters() {
    const [disasters, setDisasters] = useState([]);
    const [currIndex, setCurrIndex] = useState(0);
    const [filteredDisasters, setFilteredDisasters] = useState([]);
    const [filterSelected, setFilterSelected] = useState([]);
    const navigate = useNavigate();

    // Fetch disasters on mount 
    useEffect(() => {
        // Add parameters if necessary
        fetch(`${BASE_URL}/disasters`) // Ex. /disasters?limit=1 
            .then((result) => result.json())
            .then((result) => {
              setDisasters(result);
              setFilteredDisasters(result);
            })
            .then((result) => {
              setDisasters(result);
              setFilteredDisasters(result);
            })
            .catch(console.error);
    }, [])


    if(!disasters && !filteredDisasters) {
      return <div>Loading...</div>
    }

    const navigateToDisaster = (disaster) => {
      navigate(`/AllDisasters/${disaster.name}`, { state: disaster });
    }


    const back = () => {
      if(currIndex > 0) {
        setCurrIndex(currIndex - 4);
      }
    }

    const next = () => {
      if (currIndex < disasters.length - 1) {
        setCurrIndex(currIndex + 4);
      }
    };

    const filterChange = (e) => {
      if(e.target.checked) {
        setFilterSelected([...filterSelected, e.target.value])
      } else {
        setFilterSelected(filterSelected.filter((filterID) => filterID !== e.target.value))
      }
    }

    useEffect(() => {
      console.log(filterSelected);
      if(filterSelected.length === 0) {
        setFilteredDisasters(disasters);
      } else {
        const newDisasters = filterSelected.map((filterID) =>
          disasters.filter(disaster => disaster.overallSentiment === filterID)
        );
        setFilteredDisasters(newDisasters.flat());
      }
    }, [filterSelected])

    return (
      <div className="flex flex-col mt-30 min-w-screen min-h-screen h-auto absolute left-0 right-0 px-10 md:px-20 pb-10 overflow-x-hidden">
          <h1 className="text-4xl font-bold text-left">All Disasters</h1>
          <div className="flex flex-col gap-y-10 md:flex-row w-full gap-x-10">
          <div className="flex flex-col items-start gap-x-2 w-1/2 gap-y-3 mt-20">

            <h3 className="border border-[#D4D4D4] rounded-md text-md py-2 px-4">Overall Sentiment</h3>
            <div className="flex flex-row items-center gap-x-2">
              <input
                type="checkbox"
                value="positive"
                onChange={filterChange}
                id="positive"
              />
              <p>Positive</p>
            </div>
            <div className="flex flex-row items-center gap-x-2">
              <input
                type="checkbox"
                value="neutral"
                onChange={filterChange}
                id="neutral"
              />
              <p>Neutral</p>
            </div>
            {/* <div className="flex flex-row items-center gap-x-2">
              <input
                type="checkbox"
                value="negative"
                onChange={negativeSelected}
                id="negative"
              />
              <p>Negative</p>
            </div> */}
          
          </div>
          
              
              <div className="flex flex-col w-full md:mt-15">
                {filteredDisasters.slice(currIndex,currIndex + 4).map((disaster) => (
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
        
}