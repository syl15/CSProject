import React, {useState} from 'react';
import { MagnifyingGlassIcon } from '@radix-ui/react-icons';

import { BASE_URL } from "../config.js";

export default function Searchbar({ setResults, onFocus }) {
    const [input, setInput] = useState("");
    
    const fetchData = (value) => {
        fetch(`${BASE_URL}/disasters`) 
            .then((response) => response.json())
            .then((json) => {
                const results = json.filter((disaster) => (
                    value && disaster.name && 
                    disaster.name.toLowerCase().includes(value.toLowerCase())
                ));
                setResults(results);
            });
        
    };

    const handleChange = (value) => {
        setInput(value);
        fetchData(value);
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