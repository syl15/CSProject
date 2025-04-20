import React, {useEffect, useRef, useState} from 'react';
import SearchResult from './SearchResult';


export default function SearchResultsList( {results, onClickOutside, onClickDisaster}) {
    const wrapperRef = useRef(null);
 
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
                onClickOutside();
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [onClickOutside]);

    return (
        <div>
            {/* {showMenu && */}
            <div ref={wrapperRef} className="results-list absolute min-w-62.5 text-left overflow-auto h-auto max-h-60 overflow-y-auto bg-white border border-gray-300 z-50">
                {results.length === 0 ? (
                    <div className="px-4 py-2 text-gray-500 text-sm"> No results found </div>
                        ) : (
                    results.map((result, id) => (

                        <SearchResult result={result} key={id} onClick={onClickDisaster}/>
                    ))
                )}
            </div>
            {/* } */}
        </div>
    );
}
