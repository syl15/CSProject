import React from 'react';
import { Chart as ChartJS } from "chart.js/auto";
import { Doughnut } from "react-chartjs-2";

export default function PieChart() {
  return (
    <div className="flex flex-col flex-start border border-[#D4D4D4] rounded-md mt-15 text-left p-4">
        <h3>Sentiment Trend</h3>
        <h1 className="text-3xl font-bold mt-2">Pie chart here!</h1>  

        <Doughnut
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
