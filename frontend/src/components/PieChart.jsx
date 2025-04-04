import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function PieChart({sentiment}) {
  const total = (sentiment.positive + sentiment.negative + sentiment.neutral);
  const positive = Math.ceil((sentiment.positive/total) * 100);
  const negative = Math.ceil((sentiment.negative/total) * 100);
  const neutral = Math.ceil((sentiment.neutral/total) * 100);

  return (
    <div className="flex flex-col border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-4 gap-y-2 h-[25rem] w-full">
      <div className="w-full border-b-1 border-[#D4D4D4]">
        <h3 className="pb-2">Sentiment Trend</h3>
      </div>

      <div className="w-full h-[20rem] flex justify-center items-center">
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
      </div>
    </div>
  );
}
