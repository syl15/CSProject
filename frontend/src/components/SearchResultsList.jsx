import React, {useEffect, useRef} from 'react';
import SearchResult from './SearchResult';

export default function SearchResultsList( {results, onClickOutside}) {
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

            <div ref={wrapperRef} className="results-list absolute min-w-62.5 text-left overflow-auto h-auto max-h-60 overflow-y-auto bg-white border border-gray-300">
                {results.map((result, id) => (
                    <SearchResult result={result} key={id} />
                ))}
            </div>
    );
}
