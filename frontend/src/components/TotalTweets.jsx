import React from 'react'

export default function TotalTweets({total}) {
  console.log
  return (
    <div className="flex flex-col flex-start border border-[#D4D4D4] rounded-md mt-15 text-left p-4">
        <h3>Total Posts</h3>
        <h1 className="text-3xl font-bold mt-2">
          {total ? (
            total
          ) : (
            <p>No data</p>
          )}
        </h1>
    </div>
  )
}