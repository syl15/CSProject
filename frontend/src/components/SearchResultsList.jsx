import React from 'react';
import SearchResult from './SearchResult';

export default function SearchResultsList( {results}) {
    return (
    <div className = "absolute top-full left-0 w-full z-50 max-h-60 overflow-y-auto">
        { results.map((result, id) => {
            return <SearchResult result = {result} key = {id}/>; 
        })}
        
    </div> 
    );
}
