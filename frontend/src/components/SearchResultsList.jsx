import React from 'react';
import SearchResult from './SearchResult';

export default function SearchResultsList( {results}) {
    return (
    <div className = "results-list fixed -mt-[0.5]">
        { results.map((result, id) => {
            return <SearchResult result = {result} key = {id}/>; 
        })}
        
    </div> 
    );
}
