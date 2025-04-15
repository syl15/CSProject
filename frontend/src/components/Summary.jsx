import React from 'react'

export default function Summary({summary}) {
  return (
    <div className="flex flex-col flex-start border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-4 gap-y-2 w-full lg:w-1/2">
        <div className="border-b-1 border-[#D4D4D4]">
            <h3 className="pb-2">Summary</h3>
        </div>
        
          {summary ? (
            <div className="flex flex-wrap p-2">{summary}</div>
          ) : (
            <div className="flex flex-wrap justify-center items-center leading-80">No data</div>
          )}
        
    </div>
  );
}