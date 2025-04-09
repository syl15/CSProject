import React, {useState, useEffect} from "react";

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