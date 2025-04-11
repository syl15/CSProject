/*import React, {useState, useEffect} from "react";

const BASE_URL = "http://127.0.0.1:5001"; // Flask API URL

const TestAPI = () => {
    const [disasters, setDisasters] = useState([]);
    const [recentDisaster, setRecentDisaster] = useState(null); 

    // Fetch disasters on mount 
    useEffect(() => {
        // Add parameters if necessary
        fetch(`${BASE_URL}/disasters`) // Ex. disasters?limit=1
            .then((result) => result.json())
            .then(setDisasters)
            .catch(console.error);
        
        fetch(`${BASE_URL}/disasters/recent`)
            .then((result) => result.json())
            .then(setRecentDisaster)
            .catch(console.error);

    }, [])

    return (
        <div>
            <h2>Test Flask API</h2>
            <h3>Recent Disaster</h3>
            <pre>{recentDisaster ? JSON.stringify(recentDisaster, null, 2) : "No data"}</pre>

            <h3>Disasters</h3>
            <pre>{disasters.length ? JSON.stringify(disasters, null, 2) : "No data"}</pre>        
        </div> 
    );
}
 
export default TestAPI;

*/

import React, { useState, useEffect } from "react";

const MOCK_DATA_URL = "/mock_disaster_data.json"; // Path to mock data

const TestAPI = () => {
    const [disasters, setDisasters] = useState([]);
    const [recentDisaster, setRecentDisaster] = useState(null); 

    // Fetch mock data on mount
    useEffect(() => {
        fetch(MOCK_DATA_URL)
            .then((response) => response.json())
            .then((data) => {
                setDisasters(data); // Assuming data is an array of disasters
                if (data.length > 0) {
                    setRecentDisaster(data[0]); // Assume first item is the most recent
                }
            })
            .catch(console.error);
    }, []);

    return (
        <div>
            <h2>Test Mock API</h2>
            <h3>Recent Disaster</h3>
            <pre>{recentDisaster ? JSON.stringify(recentDisaster, null, 2) : "No data"}</pre>

            <h3>Disasters</h3>
            <pre>{disasters.length ? JSON.stringify(disasters, null, 2) : "No data"}</pre>
        </div>
    );
};

export default TestAPI;
