import React from "react";
import { useNavigate, Link } from 'react-router-dom';
import { useEffect } from "react";

export default function SearchResult( {result, onClick}) {
    const navigate = useNavigate();
    
    const navigateToDisaster = (disaster) => {
        onClick();
        navigate(`/AllDisasters/${disaster.name}`, { state: disaster });        
    };

    

    return (
        <div 
            className="search-result px-4 py-2 cursor-pointer text-left w-full hover:text-indigo-500"
            onClick={() => navigateToDisaster(result)}
        >
            {result.name}
        </div>
    );
}