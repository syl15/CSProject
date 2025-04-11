import React from 'react'
import Navbar from './components/Navbar'
import DisasterCard from './components/DisasterCard'
import FilterColumn from './components/FilterColumn'
import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard'
import { Collapsible } from "radix-ui";
import {
	CaretDownIcon, CheckIcon, Cross2Icon, RowSpacingIcon
} from "@radix-ui/react-icons";

export default function AllDisasters() {
    const [disasters, setDisasters] = useState([]);
    const [currIndex, setCurrIndex] = useState(0);
    const [filteredDisasters, setFilteredDisasters] = useState([]);
    const [sentimentFilter, setSentimentFilter] = useState([]);
    const [eventFilter, setEventFilter] = useState([]); 
    const [openSentiment, setOpenSentiment] = useState(false);
    const [openEvent, setOpenEvent] = useState(false);
    const sentimentTypes = ["positive", "neutral", "negative"];
    const eventTypes = ["earthquake", "hurricane", "wildfire"]
    
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

    const filterUpdate = (e, filters, setFilters) => {
      if(e.target.checked) {
        setFilters([...filters, e.target.value])
      } else {
        setFilters(filters.filter((filterID) => filterID !== e.target.value))
      }
    }

    useEffect(() => {
      if(sentimentFilter.length === 0 && eventFilter.length === 0) {
        setFilteredDisasters(disasters);
      } 
      else {
        let resultArr = disasters;
        resultArr = filterBySentiment(resultArr);
        console.log(resultArr);
        resultArr = filterByEvent(resultArr.flat());
        console.log(resultArr);
        setFilteredDisasters(resultArr.flat().sort(function(a, b) {
          return a.id - b.id;
        }));

      }
    }, [sentimentFilter, eventFilter])

    const filterBySentiment = (filteredArray) => {
      if(sentimentFilter.length === 0) {
        return filteredArray;
      }
      else {
        filteredArray = sentimentFilter.map((filterID) => (
          filteredArray.filter(disaster => disaster.overallSentiment === filterID)
        ))        
        return filteredArray;
      }
      
    };

    const filterByEvent = (filteredArray) => {
      if(eventFilter.length === 0) {
        return filteredArray;
      }
      else {
        
        filteredArray = eventFilter.map((filterID) => (
          filteredArray.filter(disaster => disaster.eventType === filterID)
        ))
        return filteredArray;
      }
      
    };

    return (
      <div className="flex flex-col mt-30 min-w-screen min-h-screen h-auto absolute left-0 right-0 px-10 md:px-20 pb-10 overflow-x-hidden">
          <h1 className="text-4xl font-bold text-left">All Disasters</h1>
          <div className="flex flex-col gap-y-10 md:flex-row w-full gap-x-10">
          <div className="flex flex-col items-start gap-x-2 w-1/2 gap-y-3 mt-20">
            <Collapsible.Root
              className="relative"
              open={openSentiment}
              onOpenChange={setOpenSentiment}
            >
              <Collapsible.Trigger className="flex flex-row justify-center items-center gap-x-2 border border-[#D4D4D4] rounded-md bg-white">
              Overall Sentiment
                {openSentiment ? <Cross2Icon /> : <CaretDownIcon />}
              </Collapsible.Trigger>
                
                  
              <Collapsible.Content className="flex flex-col flex-start border border-[#D4D4D4] rounded-md gap-y-1 text-left p-4 mt-3 ">
                {sentimentTypes.map((sentimentID) => (
                  <div className="flex flex-row items-center gap-x-2">
                    <input
                      type="checkbox"
                      value={sentimentID}
                      onChange={(e) => filterUpdate(e, sentimentFilter, setSentimentFilter)}
                      id={sentimentID}
                    />
                    <p>{sentimentID}</p>
                  </div>
                ))}
              </Collapsible.Content>
            </Collapsible.Root>    

            
            <Collapsible.Root
              className="relative"
              open={openEvent}
              onOpenChange={setOpenEvent}
            >
              <Collapsible.Trigger className="flex flex-row justify-center items-center gap-x-2 border border-[#D4D4D4] rounded-md bg-white">
              Event Type
                {openEvent ? <Cross2Icon /> : <CaretDownIcon />}
              </Collapsible.Trigger>
                
                  
              <Collapsible.Content className="flex flex-col flex-start border border-[#D4D4D4] rounded-md gap-y-1 text-left p-4 mt-3 ">
                {eventTypes.map((eventID) => (
                  <div className="flex flex-row items-center gap-x-2">
                    <input
                      type="checkbox"
                      value={eventID}
                      onChange={(e) => filterUpdate(e, eventFilter, setEventFilter)}
                      id={eventID}
                    />
                    <p>{eventID}</p>
                  </div>
                ))}
              </Collapsible.Content>
            </Collapsible.Root>   
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