import React from 'react'

export default function Summary() {
  return (
    <div className="flex flex-col flex-start border border-[#D4D4D4] rounded-md mt-5 md:mt-15 text-left p-4 gap-y-2 max-w-xl">
        <div className="border-b-1 border-[#D4D4D4]">
            <h3 className="pb-2">Summary</h3>
        </div>
        <div className="flex flex-wrap p-2">
        The California Wildfires happened from January 7th, 2025 to January 31st 2025. The most affected regions are: Pacific Palisades, Malibu, Topanga, Pasadena, Altadena, Sierra Madre, and La Canada Flintridge.

        Many tweets express sadness, frustration, and grief. There’s strong support for firefighters and calls for donations to help victims.
        </div>
    </div>
  );
}
