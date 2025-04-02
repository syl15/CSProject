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
    <div className="flex flex-col mt-30 overflow-hidden">
        <div className="flex flex-col gap-y-2">
            <h1 className="text-4xl font-bold text-left">Overview</h1>
            <h3 className="text-md text-left">February 16th, 2025 - February 22nd, 2025</h3>
        </div>
        <div className="row-one flex flex-col md:flex-row md:gap-x-10">
            <TotalTweets/>
            {/* <OverallSentiment/> */}
            <Severity/>
        </div>
        <div className="row-two flex flex-col md:flex-row md:gap-x-10">
            <PieChart/>
            <Map/>
        </div>
        <div className="row-three flex flex-col md:flex-row md:gap-x-10">
            <TopTweets/>
        </div>
        <div className="row-three flex flex-col md:flex-row md:gap-x-10">
            <WordMap/>
        </div>

        
    </div>
  )
}