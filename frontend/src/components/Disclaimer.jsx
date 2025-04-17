import React from 'react'
import { InfoCircledIcon } from "@radix-ui/react-icons";

export default function Disclaimer() {
    //0644cf
    //c5d7f8
    //edf5ff
    
  return (
    <div className="flex flex-col flex-start justify-center bg-[#edf5ff] border border-1 border-[#0644cf] rounded-md text-left p-6 gap-y-5 min-w-screen absolute left-0 right-0 max-h-10 mb-10">
        <div className="flex flex-row items-center gap-x-2 pl-3 md:pl-10">
            <InfoCircledIcon className="fill-[#0644cf]"/>
            This is the most recent disaster.
        </div>
    </div>
  );
}
