import React from 'react'
import TotalTweets from './TotalTweets'
import Severity from './Severity'
import TopTweets from './TopTweets'
import Summary from './Summary'
import Map from './Map'
import PieChart from './PieChart'
import AddedDate from './AddedDate'
import { useLocation } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { BASE_URL } from "../config";
import Disclaimer from './Disclaimer'


export default function Dashboard({disaster, isMostRecent}) {
    const location = useLocation();
    const currDisaster = location.state || disaster; 
   
   const [disasterInfo, setDisasterInfo] = useState();
   // Fetch disasters on mount 
    useEffect(() => {
        // Add parameters if necessary
        fetch(`${BASE_URL}/disasters/${currDisaster.id}`) // Ex. /disasters?limit=1 
            .then((result) => result.json())
            .then((data) => {
                console.log(data);
                setDisasterInfo(data)
            })
            .catch(console.error);
    }, [currDisaster?.id]);
   
    if(!disasterInfo) {
        return <div className="mt-30">Loading...</div>
    }
    const start = new Date(`${disasterInfo.startDate}T00:00:00`).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric"});

    return (
        <div className="flex flex-col mt-[3.03rem] md:mt-13 w-screen h-auto absolute left-0 right-0 px-10 md:px-20 pb-10 md:pb-40 overflow-x-hidden">
            
            {isMostRecent && <Disclaimer/>}
            <div className="flex flex-col gap-y-2 mt-25">
                <h1 className="text-4xl font-bold text-left">{disasterInfo.name}</h1>
            </div>
            <div className="row-one flex flex-col lg:flex-row lg:gap-x-10">
                <AddedDate dateAdded={start}/>
                <TotalTweets total={disasterInfo.totalPosts}/>
                <Severity severity={disasterInfo.severity}/>
            </div>
            <div className="row-two flex flex-col lg:flex-row lg:gap-x-10">
                <Summary summary={disasterInfo.summary}/>
                <PieChart sentiment={disasterInfo.sentiment}/>
            </div>
            <div className="row-three flex flex-col overflow-hidden w-full lg:flex-row md:gap-x-10">
                <Map location={disasterInfo.location}/>
                <TopTweets tweetsList={disasterInfo.posts}/>
            </div>
        </div>
    )
}