import React from 'react'

export default function DisasterCard() {
  return (
    <div className="flex flex-col flex-start border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-6 gap-y-5 max-w-xl w-full">
        <div className="row-one flex flex-col flex-wrap">
            <h1 className="text-2xl font-bold text-left">Aegean Sea Earthquake</h1>
            <h3 className="text-md">October 30th, 2020</h3>
        </div>
        <div className="row-two">
            <p><b>Disaster Type:</b> Earthquake</p>
            <p><b>Overall Sentiment:</b> Negative</p>
        </div>
    </div>
  );
}
