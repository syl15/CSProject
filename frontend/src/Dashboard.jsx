import React from 'react'
import TotalTweets from './TotalTweets'
import OverallSentiment from './OverallSentiment'
import Severity from './Severity'
import TopTweets from './TopTweets'
import PieChart from './PieChart'
import Map from './Map'
import WordMap from './WordMap'

export default function Dashboard() {
  return (
    <div className="flex flex-col mt-30 left-0 w-screen absolute left-0 right-0 overflow-x-hidden px-10 pb-10">
        <div className="flex flex-col gap-y-2">
            <h1 className="text-4xl font-bold text-left">Overview</h1>
            <h3 className="text-md text-left">February 16th, 2025 - February 22nd, 2025</h3>
        </div>
        <div className="row-one flex flex-col md:flex-row md:gap-x-10">
            <TotalTweets/>
            {/* <OverallSentiment/> */}
            <Severity/>
        </div>
        <div className="row-three flex flex-col md:flex-row">
            <TopTweets/>
        </div>
        <div className="row-three flex flex-col md:flex-row md:gap-x-10">
            <WordMap/>
        </div>

        
    </div>
  )
}