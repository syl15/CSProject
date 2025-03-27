import React from 'react';
import { Chart as ChartJS } from "chart.js/auto";
import { Doughnut, Pie } from "react-chartjs-2";

// had to  "npm install react-chartjs-2 chart.js"   

export default function PieChart() {
  return (
    <div className="flex flex-col items-start border border-[#D4D4D4] rounded-md mt-4 text-left p-4">
        <h3>Sentiment Trend</h3>

        <Pie
          data={{
            labels: ["Positive", "Netural", "Negative"],
            datasets: [
                {
                  label: "Percentage",
                  data: [10, 20, 30], // Fixed structure
                  backgroundColor: [
                    "rgba(185,230,191, 0.8)", // Postive
                    "rgba(234, 234, 234, 0.8)", // Netural
                    "rgba(255, 202, 202, 0.8)", // Negative
                  ]
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
          }}
        />       
    </div>
  );
}
