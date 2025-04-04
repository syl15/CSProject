import React from 'react'
import { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard'
const BASE_URL = "http://127.0.0.1:5001"; // Flask API URL

export default function RecentDisaster() {
    const [recentDisaster, setRecentDisaster] = useState(null); 

    // Fetch disasters on mount 
    useEffect(() => {        
        fetch(`${BASE_URL}/disasters/recent`)
            .then((result) => result.json())
            .then(setRecentDisaster)
            .catch(console.error);

    }, [])

    if(!recentDisaster) {
        return <div>Loading...</div>
    }
    return (
        <Dashboard disaster={recentDisaster}/>
    )
}