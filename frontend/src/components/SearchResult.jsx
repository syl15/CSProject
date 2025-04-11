import React from "react";
<<<<<<< HEAD
=======

// import "./SearchResult.css";
>>>>>>> c396508 (added search bar)
export default function SearchResult( {result}) {
    return (
    <div 
        className = "search-result"
        onClick = {(e) => alert(`You clicked on ${result.name}`)} // Route this to the correct disaster
    >
        {result.name}
    </div>
    );
}