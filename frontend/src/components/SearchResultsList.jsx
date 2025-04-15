import React from 'react';
import SearchResult from './SearchResult';

export default function SearchResultsList( {results}) {
    return (
    <div className="results-list absolute max-w-62.5 text-left overflow-auto h-auto">
    { results.map((result, id) => {
            return <SearchResult result = {result} key = {id}/>; 
        })}    
    </div> 
    );
}
