import React from 'react'
import TotalTweets from './TotalTweets'
import Severity from './Severity'
import TopTweets from './TopTweets'
import Summary from './Summary'
import Map from './Map'
import PieChart from './PieChart'
import { useLocation } from 'react-router-dom'

export default function Dashboard({disaster}) {
    const location = useLocation();
    const currDisaster = location.state || disaster; 
    const start = new Date(`${currDisaster.startDate}T00:00:00`).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric"});
  return (
    <div className="flex flex-col mt-30 w-screen h-auto absolute left-0 right-0 px-10 md:px-20 pb-10 md:pb-40 overflow-x-hidden">
        <div className="flex flex-col gap-y-2">
            <h1 className="text-4xl font-bold text-left">{currDisaster.name}</h1>
            <h3 className="text-lg text-left">{start}</h3>
        </div>
        <div className="row-one flex flex-col lg:flex-row lg:gap-x-10">
            <TotalTweets total={currDisaster.totalPosts}/>
            {/* <Severity severity={currDisaster.severity}/> */}
        </div>
        <div className="row-two flex flex-col lg:flex-row lg:gap-x-10">
            <Summary summary={currDisaster.summary}/>
            <PieChart sentiment={currDisaster.sentiment}/>
        </div>
        <div className="row-three flex flex-col overflow-hidden w-full lg:flex-row md:gap-x-10">
            <Map location={currDisaster.location}/>
            {currDisaster.posts ? (
                <TopTweets tweetsList={currDisaster.posts}/>
            ) : (
                <p>No data</p>
            )}
            {/* <TopTweets tweetsList={currDisaster.topTweets}/> */}
        </div>
    </div>
  )
}