import React from 'react'

export default function OverallSentiment() {
  return (
    <div className="flex flex-col flex-start border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-4 gap-y-2">
        <h3>Overall Sentiment</h3>
        <div className="sentiment flex flex-col md:flex-row gap-y-4 md:gap-x-10">
            <div className="negative flex flex-row justify-center items-center gap-x-3 bg-[#FFCACA] p-4 rounded-[10px]">
                <h3>Negative</h3>
                <h1 className="text-3xl font-bold">60%</h1>
            </div>
            <div className="neutral flex flex-row justify-center items-center gap-x-3 bg-[#EAEAEA] p-4 rounded-[10px]">
                <h3>Neutral</h3>
                <h1 className="text-3xl font-bold">35%</h1>
            </div>
            <div className="positive flex flex-row justify-center items-center gap-x-3 bg-[#CAFFD2] p-4 rounded-[10px]">
                <h3>Positive</h3>
                <h1 className="text-3xl font-bold">5%</h1>
            </div>
        </div>
    </div>
  )
}
