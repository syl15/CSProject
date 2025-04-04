import React from 'react'
import TotalTweets from './TotalTweets'
import OverallSentiment from '../OverallSentiment'
import Severity from './Severity'
import TopTweets from './TopTweets'
import Summary from './Summary'

export default function Dashboard({disaster}) {

  return (
    <div className="flex flex-col mt-30 w-screen h-auto absolute left-0 right-0 px-10 md:px-20 pb-10 overflow-x-hidden">
        <div className="flex flex-col gap-y-2">
            <h1 className="text-4xl font-bold text-left">{disaster.name}</h1>
            <h3 className="text-md text-left">{disaster.startDate} - {disaster.endDate}</h3>
        </div>
        <div className="row-one flex flex-col md:flex-row md:gap-x-10">
            <TotalTweets total={disaster.totalTweets}/>
            {/* <OverallSentiment/> */}
            <Severity severity={disaster.severity}/>
        </div>
        <div className="row-two flex flex-col md:flex-row md:gap-x-10">
            <Summary summary={disaster.summary}/>
        </div>
        <div className="row-three flex flex-col overflow-hidden w-full md:flex-row md:gap-x-10">
            <TopTweets tweetsList={disaster.topTweets}/>
        </div>
        
    </div>
  )
}