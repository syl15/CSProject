import React from 'react'
import { useState, useEffect } from 'react';
import Dashboard from './components/Dashboard'
import { BASE_URL } from "./config";

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