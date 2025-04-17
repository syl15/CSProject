import React from 'react'
import ToolTip from './ToolTip';

export default function Severity({severity}) {
  const paragraph = "Severity score combines the proportion of negative posts with the intensity of the median sentiment. Severity = sentiment balance + sentiment intensity. Scale: 1 = minor, 3 = moderate, 5 = critical"
  return (
    <div className="flex flex-col flex-start border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-4 gap-y-2">
        <div className="flex flex-row gap-x-2 items-center justify-between">
          <h3>Severity</h3>
          <ToolTip paragraph={paragraph}/>
        </div>
        <h1 className="text-3xl font-bold">
          {severity ? (
            severity
            ) : (
              <p>No data</p>
          )}
        </h1>
    </div>
  );
}
