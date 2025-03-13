import React from 'react'
import TotalTweets from './TotalTweets'

export default function Dashboard() {
  return (
    <div className="flex flex-col mt-30">
        <div className="flex flex-col gap-y-2">
            <h1 className="text-4xl font-bold text-left">Overview</h1>
            <h3 className="text-md text-left">February 16th, 2025 - February 22nd, 2025</h3>
        </div>
        <TotalTweets/>
    </div>
  )
}