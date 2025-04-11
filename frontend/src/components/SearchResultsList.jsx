import React from 'react';
import SearchResult from './SearchResult';

export default function SearchResultsList( {results}) {
    return (
    <div className = "results-list">
        { results.map((result, id) => {
            return <SearchResult result = {result} key = {id}/>; 
        })}
        
    </div> 
    );
}


/*
import React from 'react';

export default function SearchResultsList({ results }) {
    return (
        <div className="absolute top-full left-0 right-0 z-50 mt-1">
            <div className="border border-[#D4D4D4] rounded-sm bg-white shadow-md">
                {results.length > 0 ? (
                    results.map((result) => (
                        <div 
                            key={result.id}
                            className="px-4 py-2 hover:bg-[#F6F6F6] cursor-pointer text-sm"
                        >
                            {result.name}
                        </div>
                    ))
                ) : (
                    <div className="px-4 py-2 text-sm text-gray-500">
                        No results found
                    </div>
                )}
            </div>
        </div>
    );
}
*/