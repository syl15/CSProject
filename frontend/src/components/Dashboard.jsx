import React from 'react'
import TotalTweets from './TotalTweets'
import Severity from './Severity'
import TopTweets from './TopTweets'
import Summary from './Summary'
import Map from './Map'
import PieChart from './PieChart'

export default function Dashboard({disaster}) {
    const start = new Date(`${disaster.startDate}T00:00:00`).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric"});
    const end = new Date(`${disaster.endDate}T00:00:00`).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric"});
  return (
    <div className="flex flex-col mt-30 w-screen h-auto absolute left-0 right-0 px-10 md:px-20 pb-10 md:pb-40 overflow-x-hidden">
        <div className="flex flex-col gap-y-2">
            <h1 className="text-4xl font-bold text-left">{disaster.name}</h1>
            <h3 className="text-lg text-left">{start} - {end}</h3>
        </div>
        <div className="row-one flex flex-col lg:flex-row lg:gap-x-10">
            <TotalTweets total={disaster.totalTweets}/>
            <Severity severity={disaster.severity}/>
        </div>
        <div className="row-two flex flex-col lg:flex-row lg:gap-x-10">
            <Summary summary={disaster.summary}/>
            <PieChart sentiment={disaster.sentiment}/>
        </div>
        <div className="row-three flex flex-col overflow-hidden w-full lg:flex-row md:gap-x-10">
            <Map location={disaster.location}/>
            <TopTweets tweetsList={disaster.topTweets}/>
        </div>
    </div>
  )
}