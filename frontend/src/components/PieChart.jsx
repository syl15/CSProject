import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
import ToolTip from "./ToolTip";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function PieChart({sentiment}) {
  
  const paragraph = "Posts are assigned a sentiment score from -1 to 1 and classified as positive (≥ 0.05), neutral (-0.05 to 0.05), or negative (≤ -0.05)."
  let positive, negative, neutral;

  if(sentiment) {
    const total = (sentiment.positive + sentiment.negative + sentiment.neutral);
    positive = Math.ceil((sentiment.positive/total) * 100);
    negative = Math.ceil((sentiment.negative/total) * 100);
    neutral = Math.ceil((sentiment.neutral/total) * 100);
  }

  return (
    <div className="flex flex-col border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-4 gap-y-2 h-[25rem] w-full">
        <div className="border-b-1 border-[#D4D4D4] pb-2">
          <div className="flex flex-row gap-x-2 items-center justify-between">
            <h3>Sentiment Trend</h3>
            <ToolTip paragraph={paragraph}/>
          </div>
        </div>

      <div className="w-full h-[20rem] flex justify-center items-center">
      {sentiment ? (
        <Pie
          data={{
            labels: ["Positive", "Neutral", "Negative"],
            datasets: [
              {
                label: "Percentage",
                data: [positive, neutral, negative], 
                backgroundColor: [
                  "rgba(185,230,191, 0.8)", // Positive
                  "rgba(234, 234, 234, 0.8)", // Neutral
                  "rgba(255, 202, 202, 0.8)", // Negative
                ],
              },
            ],
          }}
          options={{
            responsive: true, 
            maintainAspectRatio: false, 
            plugins: {
              tooltip: {
                callbacks: {
                  label: function (tooltipItem) {
                    return ` ${tooltipItem.raw}%`;
                  },
                },
              },
            },
          }}
        />
      ) : (
        <p>No data</p>
      )}
        
      </div>
    </div>
  );
}
