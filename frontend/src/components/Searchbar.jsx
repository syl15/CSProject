/*import React, {useState} from 'react';
import { MagnifyingGlassIcon } from '@radix-ui/react-icons';

export default function Searchbar({ setResults }) {
    const [input, setInput] = useState("");

    const fetchData = (value) => {
        fetch("https://jsonplaceholder.typicode.com/users")
            .then((response) => response.json())
            .then((json) => {
                const results = json.filter((user) => (
                    value && user && user.name && 
                    user.name.toLowerCase().includes(value.toLowerCase())
                ));
                setResults(results);
            });
    };

    const handleChange = (value) => {
        setInput(value);
        fetchData(value);
    };

    return (
        <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-[11px]"/>
            <input
                className="h-[38px] w-full pl-8 pr-2 border border-[#D4D4D4] rounded-sm text-sm focus:outline-0"
                type="text"
                placeholder="Search"
                value={input}
                onChange={(e) => handleChange(e.target.value)}
            />
        </div>
    );
}
*/

import React, {useState} from 'react';
import { MagnifyingGlassIcon } from '@radix-ui/react-icons';

export default function Searchbar({ setResults }) {
    const [input, setInput] = useState("");

    const fetchData = (value) => {
        fetch("https://jsonplaceholder.typicode.com/users")
            .then((response) => response.json())
            .then((json) => {
                const results = json.filter((user) => (
                    value && user && user.name && 
                    user.name.toLowerCase().includes(value.toLowerCase())
                ));
                setResults(results);
            });
    };

    const handleChange = (value) => {
        setInput(value);
        fetchData(value);
    };

    return (
        <div className="relative">
            <MagnifyingGlassIcon className="absolute left-3 top-[11px]"/>
            <input
                className="h-[38px] w-full pl-8 pr-2 border border-[#D4D4D4] rounded-sm text-sm focus:outline-0"
                type="text"
                placeholder="Search"
                value={input}
                onChange={(e) => handleChange(e.target.value)}
            />
        </div>
    );
}