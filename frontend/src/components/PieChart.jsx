import React from "react";
import { Pie } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend);

export default function PieChart() {
  return (
    <div className="flex flex-col border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-4 gap-y-2 h-[25rem] w-full">
      <div className="w-full border-b-2 border-[#D4D4D4]">
        <h3 className="pb-2">Sentiment Trend</h3>
      </div>

      {/* New container to control chart size */}
      <div className="w-full h-[20rem] flex justify-center items-center">
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
            responsive: true, // Ensures the chart adjusts to container size
            maintainAspectRatio: false, // Allows the chart to stretch to container size
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
    </div>
  );
}
