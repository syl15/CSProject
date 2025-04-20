import React from 'react'
import ToolTip from './ToolTip'

export default function TotalTweets({total}) {
  const paragraph = "Posts are related to the disaster and grouped by a clustering algorithm. Clustering may occasionally be inaccurate."
  return (
    <div className="flex flex-col flex-start border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-4">
        <div className="flex flex-row gap-x-2 items-center justify-between">
          <h3>Total Posts</h3>
          <ToolTip paragraph={paragraph}/>
        </div>
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