import React, {useState, useEffect, useRef} from 'react';
import { MagnifyingGlassIcon } from '@radix-ui/react-icons';

import { BASE_URL } from "../config.js";

export default function Searchbar({ setResults, onFocus}) {
    const [input, setInput] = useState("");
    const debounceTimeout = useRef(null);
    
    // useEffect((value) => {
    //     fetch(`${BASE_URL}/disasters`) 
    //     .then((response) => response.json())
    //     .then((json) => {
    //         const results = json.filter((disaster) => (
    //             value && disaster.name && 
    //             disaster.name.toLowerCase().includes(value.toLowerCase())
    //         ));
    //         setResults(results);
    //     })
    //     .catch(console.error);
    // }, [])

    const fetchData = (value) => {
        if (!value.trim()) {
            console.log("Skipping fetch — input is empty.");
            setResults([]);
            return;
          }
        
        console.log(`Fetching disasters for input: "${value}"`);

        fetch(`${BASE_URL}/disasters`) 
            .then((response) => response.json())
            .then((json) => {
                const results = json.filter((disaster) => (
                    value && disaster.name && 
                    disaster.name.toLowerCase().includes(value.toLowerCase())
                ));
                setResults(results);
            })
            .catch(console.error);
        
    };

    const handleChange = (value) => {
        setInput(value);
    
        clearTimeout(debounceTimeout.current);
        debounceTimeout.current = setTimeout(() => {
          fetchData(value);
        }, 100); // wait 200ms after typing stops

    };

    return (
        <div className="relative focus:outline-hidden z-50">
            <MagnifyingGlassIcon className="absolute left-3 top-[11px]"/>
            <input
                className="h-[38px] w-full pl-8 pr-2 border border-[#D4D4D4] text-sm focus:outline-none rounded-sm"
                type="text"
                placeholder="Search"
                value={input}
                onChange={(e) => handleChange(e.target.value)}
                onFocus = {onFocus}
            />
        </div>
    );
}