import React from 'react'

export default function DisasterCard({disaster}) {
  const start = new Date(`${disaster.startDate}T00:00:00`).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric"});
  const end = new Date(`${disaster.endDate}T00:00:00`).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric"});
  const maxSentiment = Math.max(...Object.values(disaster.sentiment));
  const overall = Object.keys(disaster.sentiment).find(key => disaster.sentiment[key] === maxSentiment);
  
  return (

    <div className="flex flex-col flex-start border border-[#D4D4D4] rounded-md  text-left p-6 gap-y-5 max-w-xl">
        <div className="row-one flex flex-col flex-wrap">
            <h1 className="text-2xl font-bold text-left">{disaster.name}</h1>
            {/* <h3 className="text-md">{start}</h3> */}
        </div>
        <div className="row-two">
            {/* not in mock api */}
            <p><b>Disaster Type:</b> Earthquake</p> 
            <p><b>Overall Sentiment:</b> {overall}</p>
        </div>
    </div>
  );
}
