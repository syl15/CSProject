import React from 'react';
import SearchResult from './SearchResult';

export default function SearchResultsList( {results}) {
    return (
    <div className="results-list fixed -mt-[0.5] max-h-60 max-w-62.5 overflow-y-auto text-left">

        { results.map((result, id) => {
            return <SearchResult result = {result} key = {id}/>; 
        })}
        
    </div> 
    );
}