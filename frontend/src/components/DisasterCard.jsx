import React from 'react'

export default function DisasterCard({disaster}) {
  const start = new Date(`${disaster.startDate}T00:00:00`).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric"});    
  function getBackgroundColor(disaster) {
    if(disaster.overallSentiment) {
      if(disaster.overallSentiment === "neutral") {
        return '#ffe5a0';
      }
      else if(disaster.overallSentiment === "positive") {
        return '#d4edbc';
      }
      else {
        return '#ffcfc9';
      }
    }
    else {
      return '#FFFFFF';
    }
  }

  return (

    <div className="flex flex-col flex-start border border-[#D4D4D4] rounded-md  text-left p-6 gap-y-5 max-w-xl">
        <div className="row-one flex flex-col flex-wrap">
            <h1 className="text-2xl font-bold text-left">{disaster.name}</h1>
            <h3 className="text-md">{start}</h3>
        </div>
        <div className="row-two flex flex-col gap-y-2">
            {/* not in mock api */}
            <p><b>Disaster Type:</b> {disaster.eventType}</p> 
            <div className="flex flex-row gap-x-2">
             <p><b>Overall Sentiment:</b></p>
             <p style={{ 'backgroundColor': getBackgroundColor(disaster) }} className="px-2 rounded-lg">{disaster.overallSentiment}</p> 
            </div>
        </div>
    </div>
  );
}
