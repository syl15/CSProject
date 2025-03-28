import React from 'react';
import { Pie } from "react-chartjs-2";

export default function PieChart() {
  return (
    <div className="flex flex-col items-start border border-[#D4D4D4] rounded-md mt-4 text-left p-4 w-[500px] h-[500px]">
      <div className="w-full border-b-2 border-[#D4D4D4]">
        <h3 className="pb-2">Sentiment Trend</h3>
      </div>

      <div style={{ position: "relative", width: "100%", height: "100%" }}>
        <Pie
          data={{
            labels: ["Positive", "Neutral", "Negative"],
            datasets: [
              {
                label: "Percentage",
                data: [10, 20, 30], // Fixed structure
                backgroundColor: [
                  "rgba(185,230,191, 0.8)", // Positive
                  "rgba(234, 234, 234, 0.8)", // Neutral
                  "rgba(255, 202, 202, 0.8)", // Negative
                ],
              },
            ],
          }}
          options={{
            plugins: {
              tooltip: {
                callbacks: {
                  label: function (tooltipItem) {
                    return ` ${tooltipItem.raw}%`; // Fixes tooltip display
                  },
                },
              },
            },
            responsive: true, // Ensures the chart adjusts to container size
            maintainAspectRatio: false, // Allows the chart to stretch to container size
          }}
        />
      </div>
    </div>
  );
}



// had to  "npm install react-chartjs-2 chart.js"   